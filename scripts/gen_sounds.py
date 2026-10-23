"""Synthesizes the Blink Wand's original sounds (no vanilla or third-party audio). Run from the project root.

Needs numpy and ffmpeg (libvorbis). Mono 44.1 kHz .ogg, two variants per event so repeats never sound looped.
  depart  ~0.35 s  filtered-noise whoosh sweeping down + a falling sine glide (the air folds shut)
  arrive  ~0.8 s   inharmonic bell partials with exponential decay, a short noise transient, a low thump
  fizzle  ~0.25 s  a falling sine that sputters out with crackle
"""
import os, subprocess, tempfile, wave
import numpy as np

SR = 44100
OUT = "src/main/resources/assets/starfall/sounds/blink"


def t(seconds):
    return np.arange(int(SR * seconds)) / SR


def lowpass(x, cutoff_curve):
    """One-pole low-pass with a time-varying cutoff (Hz per sample)."""
    y = np.zeros_like(x)
    acc = 0.0
    a = 1 - np.exp(-2 * np.pi * cutoff_curve / SR)
    for i in range(len(x)):
        acc += a[i] * (x[i] - acc)
        y[i] = acc
    return y


def fade(x, ms_in=4, ms_out=20):
    n_in, n_out = int(SR * ms_in / 1000), int(SR * ms_out / 1000)
    x[:n_in] *= np.linspace(0, 1, n_in)
    x[-n_out:] *= np.linspace(1, 0, n_out)
    return x


def depart(rng, pitch):
    tt = t(0.36)
    f = tt / tt[-1]
    noise = rng.standard_normal(len(tt))
    whoosh = lowpass(noise, 6000 * (1 - f) ** 2 + 300) * np.sin(np.pi * f) ** 0.7
    glide_freq = 1400 * pitch * (1 - 0.6 * f)
    glide = np.sin(2 * np.pi * np.cumsum(glide_freq) / SR) * (1 - f) ** 2 * 0.35
    return fade(whoosh * 1.6 + glide)


def arrive(rng, pitch):
    tt = t(0.85)
    bell = np.zeros_like(tt)
    for freq, amp, decay in [(1320, 1.0, 5.0), (1980, 0.55, 7.0), (2640, 0.35, 9.0), (3517, 0.2, 13.0)]:
        f0 = freq * pitch * (1 + rng.uniform(-0.004, 0.004))
        bell += amp * np.sin(2 * np.pi * f0 * tt + rng.uniform(0, 6.28)) * np.exp(-decay * tt)
    transient = rng.standard_normal(len(tt)) * np.exp(-tt * 70) * 0.6
    thump = np.sin(2 * np.pi * 120 * pitch * tt * (1 - 0.3 * tt)) * np.exp(-tt * 22) * 0.8
    return fade(bell * 0.45 + transient + thump, ms_in=1, ms_out=60)


def fizzle(rng, pitch):
    tt = t(0.26)
    f = tt / tt[-1]
    freq = 900 * pitch * (1 - 0.55 * f)
    tone = np.sin(2 * np.pi * np.cumsum(freq) / SR) * (1 - f) ** 1.5 * 0.5
    crackle = (rng.random(len(tt)) < 0.004 * (1 - f)) * rng.uniform(-1, 1, len(tt))
    crackle = lowpass(crackle * 3, np.full(len(tt), 5000.0))
    return fade(tone + crackle * 1.4)


def write(name, x):
    x = x / max(1e-9, np.abs(x).max()) * 0.85
    pcm = (x * 32767).astype("<i2")
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        path = tmp.name
    with wave.open(path, "wb") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes(pcm.tobytes())
    out = os.path.join(OUT, name + ".ogg")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path, "-c:a", "libvorbis", "-q:a", "5", out], check=True)
    os.remove(path)
    print("wrote", out)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    rng = np.random.default_rng(20261023)
    for i, pitch in enumerate([1.0, 1.07], start=1):
        write(f"depart{i}", depart(rng, pitch))
        write(f"arrive{i}", arrive(rng, pitch))
        write(f"fizzle{i}", fizzle(rng, pitch))

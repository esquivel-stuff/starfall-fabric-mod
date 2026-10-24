# CurseForge requirements (checked October 2026)

Sources:
- Moderation policies: https://support.curseforge.com/support/solutions/articles/9000197279-moderation-policies
- Creating a project: https://support.curseforge.com/en/support/solutions/articles/9000197241
- How to become a CurseForge author: https://blog.curseforge.com/how-to-become-a-curseforge-author/
- How to pass moderation review: https://blog.curseforge.com/how-to-pass-moderation-review-on-curseforge-2/

| Requirement | Source | Starfall |
| --- | --- | --- |
| Project avatar/logo at least 400x400, square, not a solid color, avoid webp | Moderation policies; author blog post | `logo.png`, 400x400 PNG, pixel art from the mod's own palette and Star Block texture |
| Images edited or made with AI need a disclaimer | Moderation policies | Not needed: the logo is drawn by `scripts/curseforge_logo.py` from the mod's own pixel art, and the screenshots are real game captures |
| Project name without the game name or version | Moderation policies | Name: `Starfall` |
| Summary of about one sentence, not copied from the description | Moderation policies | `summary.txt` |
| Description explains what the project functionally adds | Moderation policies | `description.md` / `description.html` / `description.txt` |
| No external download links; donation or personal links at the bottom | Moderation policies | Only a source code link, at the bottom |
| Every file needs a changelog | Moderation policies | `changelog-1.0.0.md` |
| Minecraft mods must be uploaded as JAR files | Moderation policies | `starfall-1.0.0+1.21.1-fabric.jar` |
| At least one file with release type Release | Moderation policies | Upload 1.0.0 as Release |
| Project fields: logo, name, summary, description, class, main category (plus up to 4 more), license | Creating a project | See UPLOAD_CHECKLIST.md |

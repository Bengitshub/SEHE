# Backups — frozen hardcopies of the live site

Each folder is a complete, dated snapshot taken from the outside (pages as
served by Duda), plus the widget code, paste sources and Worker at that
moment. Folders are never edited; a new backup gets a new dated folder.
Every snapshot is pinned by the commit that added it — git keeps that commit
forever, so the folder can always be retrieved even if later commits change it.

| Snapshot | Commit | Zip | What was live |
|---|---|---|---|
| `2026-09-06-live-site/` | `8fcb32c` | `SEHE-live-site-hardcopy-2026-09-06.zip` | Checkfront on six tour pages, new-app embed on Winter 2026; homepage v27 on root, v38 on /v2; journeys v22; brochure v2 |

Retrieve a snapshot as it was: GitHub → the commit above → "Browse files",
or `git checkout <commit> -- backups/<folder>`.
To also pin it with a tag/release (optional belt-and-braces): GitHub →
Releases → "Draft a new release" → tag `backup-2026-09-06-live` at that
commit. (Tags cannot be pushed from the build session; branches can.)

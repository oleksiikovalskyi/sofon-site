# Full media library — sofon.com.ua (from hosting backup)

317 original images (WordPress thumbnail-size variants deduped out — e.g. `-300x240`,
`-1024x819` suffixes stripped), ~30 MB, organized by `YYYY/MM/` upload date exactly as
stored in WordPress. Pulled from `public_html/wp-content/uploads/` inside a full cPanel
hosting-account backup the user provided (`cagefs.zip`, 2026-07-22) — NOT from the
public-page crawl (see `../images/` for that, and `../README.md` for how the two differ).

This set is significantly larger than the ~105 images referenced on the 8 live pages —
it includes real equipment photography not currently shown anywhere on the live site
(e.g. `2022/02/Capper.jpg`, `Filler.jpg`, `Labeler.jpg`, `Rinser.jpg`, `PE-Labeler.jpg` —
actual machine photos, useful for the "replace placeholder blocks with real photos"
backlog item noted in `sofon-site/CLAUDE.md`).

**Not extracted from the backup, deliberately:** anything outside `wp-content/uploads/`
— `wp-config.php` (contains live database credentials), the `mail/` mailbox archive,
`ssl/` keys, `.cagefs/` system files, or the unrelated `immach.com`/`immachcom` site
folders also present in that same backup. Those aren't relevant to the site rewrite and
some are actively sensitive — left untouched in the original zip, not copied anywhere.

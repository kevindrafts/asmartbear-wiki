# Maintaining the reading companion

Work only within the authorized repository and designated external cache. Read `AGENTS.md` and the attribution policy before changing editorial content.

1. Discover with sitemap, homepage, RSS, and article links. Normalize URLs, reconcile canonical/redirect aliases, honor robots, and never request source JSON or `/ref/` endpoints. Keep sequential requests at least 2.1 seconds apart; back off on server errors.
2. Capture HTML and the complete extracted body externally. Check dates, headings, final paragraphs, footnotes, tables, alt text, and captions. Inspect any image whose meaning is necessary but unclear; otherwise explicitly qualify the uncertainty. Never impose a body-length cutoff.
3. Read the entire source before drafting a concise original note. State the argument, an application, and a boundary. Preserve satire, historical context, model assumptions, numerical qualifications, and changed advice. Prefer paraphrase to quotation. A direct quote must be short, exact, attributed, and individually checked.
4. Bind the note's reviewed hash to the body actually read. Changes to the source invalidate the previous review. Update the external ledger, public metadata export, topic references, and synthesis affected by the changed argument.
5. Connect each note to an authored topic. A topic or guide needs multiple primary sources, meaningful connections, and explicit editorial inference. Counts are coverage targets, not reasons to add filler.
6. Run tests, stage the site, validate complete coverage and links, build strictly, and run the external-cache overlap audit. Review the complete staged diff, tracked paths, and existing Git history using `scripts.review_git`. Never print secret values.
7. When changing `site/wiki.js`, bump its query version in `mkdocs.yml` so existing readers fetch the updated asset. Verify desktop/mobile navigation and browser search, publish through the reviewed GitHub Pages workflow, then verify the deployed URL. Record exact commands and remaining gaps in `reports/completion.md`; keep `reports/build-status.md` current.

Do not introduce scheduled crawling or updates without a new request. Build CI must never fetch copyrighted article bodies. An overlap scan is a useful guard, not a substitute for editorial review of paraphrase, attribution, and quotations.

# Build status

Updated October 18, 2026. The [weekly update](podcast-update.md) adds E10 with Jessica Malnik and Mindstamp after complete transcript reading, bringing coverage to 237 reviewed sources: 227 articles and mailbags plus ten podcast episodes. Four topic pages and one guide gain connections. The blog discovery check found no new articles or changed sitemap timestamps; all nine earlier transcript bodies match their reviewed hashes. All 25 tests, the strict build, and the complete-corpus/cache audit pass; publication verification is pending.

| Phase | State |
|---|---|
| Test-first ingestion and validators | Complete; 22 Python and three JavaScript tests pass |
| Pilot extraction/read/build | Complete; 12 varied sources, full-body tail and structure checks |
| Longform discovery and classification | Complete for the essay update; 275 URL records, 227 included, 48 exclusions |
| Longform capture and reading | Complete; 227 bodies, 344,753 extracted words, zero included fetch failures; three full readings in the essay update |
| Original source notes | Complete; 227 article/mailbag notes and ten podcast notes tied to source-body hashes |
| Podcast reading | Complete; ten of ten located transcripts reviewed, 262,439 extracted words including speaker labels and timestamps |
| Cross-article synthesis | Complete; 43 topics, 10 decision guides, five reading paths |
| Static site and search | Complete; MkDocs, responsive navigation, source dates, backlinks |
| Coverage, citations, links, source overlap | Complete; 237 reviewed notes, zero errors; 51 transcript anchors verified |
| Pages publishing and deployed browser check | October 18 publication pending; earlier content and evidence deployments succeeded |

Public site: [A Smart Bear — Unofficial Field Notes](https://kevindrafts.github.io/asmartbear-wiki/). Exact commands, counts, failures, tests, and deployment evidence are in the [completion report](completion.md).

## Durable checkpoints

The pilot validated complete extraction of old/new essays, mailbags, long pages, tables, diagrams, and footnotes before completing the sequential crawl. Editorial batches reached 69, 132, then 226 reviewed notes. All extracted bodies were read; notes were manually authored after reading, never from titles alone. Topic consolidation produced 43 substantive pages, followed by ten guides and five reading paths.

Final discovery corrected the initial estimates: 14 hidden mailbags, and two off-sitemap essays (`growth-asymptote`, `swot`). These two essays have future-dated source metadata (2030), retained with an explicit caveat. Twenty legacy redirect chains were checked: one included canonical alias, 19 outside the longform boundary. No canonical duplicates in the included set.

Full source HTML and bodies remain only in `/Users/mordecai/.hermes/data/jason-cohen-source-cache`. The atomic external ledger records fetch, read, review, hash, and synthesis states; public catalog exports contain metadata only. The user separately authorized weekly local Codex updates for Sundays at 3 AM America/Chicago; no repository cron or scheduled source crawl was added.

MkDocs was selected as the approved simpler established alternative to Quartz: Markdown-first, local browser search, responsive navigation, and a small reproducible build without a vendored application.

# Build status

Updated October 17, 2026. The earlier [essay update](recent-update.md) is deployed and verified. The new [podcast batch](podcast-update.md) adds five fully read Smart Bear Live episodes, a reading index, and connections in six topics and three guides. Editorial work, 25 tests, strict build, complete-corpus/cache validation, timestamp checks, and local browser checks are complete. Staged/history review and publication remain in progress.

| Phase | State |
|---|---|
| Test-first ingestion and validators | Complete; 22 Python and three JavaScript tests pass |
| Pilot extraction/read/build | Complete; 12 varied sources, full-body tail and structure checks |
| Complete discovery and classification | Complete for this incremental check; 275 URL records, 227 included, 48 exclusions |
| Full capture and reading | Complete; 227 bodies, 344,753 extracted words, zero included fetch failures; three full readings in this update |
| Original source notes | Complete; 227 article/mailbag notes and five podcast notes tied to source-body hashes |
| Selected podcast reading | Complete; five of nine located transcripts reviewed, 140,079 extracted words including speaker labels and timestamps |
| Cross-article synthesis | Complete; 43 topics, 10 decision guides, five reading paths |
| Static site and search | Complete; MkDocs, responsive navigation, source dates, backlinks |
| Coverage, citations, links, source overlap | Complete; zero coverage, link, or overlap findings; staged/history review pending for this batch |
| Pages publishing and deployed browser check | Podcast publication pending; earlier essay release passed all 303 HTTP checks |

Public site: [A Smart Bear — Unofficial Field Notes](https://kevindrafts.github.io/asmartbear-wiki/). Exact commands, counts, failures, tests, and deployment evidence are in the [completion report](completion.md).

## Durable checkpoints

The pilot validated complete extraction of old/new essays, mailbags, long pages, tables, diagrams, and footnotes before completing the sequential crawl. Editorial batches reached 69, 132, then 226 reviewed notes. All extracted bodies were read; notes were manually authored after reading, never from titles alone. Topic consolidation produced 43 substantive pages, followed by ten guides and five reading paths.

Final discovery corrected the initial estimates: 14 hidden mailbags, and two off-sitemap essays (`growth-asymptote`, `swot`). These two essays have future-dated source metadata (2030), retained with an explicit caveat. Twenty legacy redirect chains were checked: one included canonical alias, 19 outside the longform boundary. No canonical duplicates in the included set.

Full source HTML and bodies remain only in `/Users/mordecai/.hermes/data/jason-cohen-source-cache`. The atomic external ledger records fetch, read, review, hash, and synthesis states; public catalog exports contain metadata only. No scheduled updates.

MkDocs was selected as the approved simpler established alternative to Quartz: Markdown-first, local browser search, responsive navigation, and a small reproducible build without a vendored application.

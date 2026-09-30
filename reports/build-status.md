# Build status

Updated September 30, 2026. Execution and public publishing to `kevindrafts/asmartbear-wiki` were explicitly authorized; the earlier plan's scoping-only language was superseded.

| Phase | State |
|---|---|
| Test-first ingestion and validators | Complete; 19 Python and three JavaScript tests pass |
| Pilot extraction/read/build | Complete; 12 varied sources, full-body tail and structure checks |
| Complete discovery and classification | Complete; 274 URL records, 226 included, 48 exclusions |
| Full capture and reading | Complete; 226 bodies, 343,448 extracted words, zero included fetch failures |
| Original article notes | Complete; 226 reviewed notes tied to source-body hashes |
| Cross-article synthesis | Complete; 43 topics, 10 decision guides, five reading paths |
| Static site and search | Complete; MkDocs, responsive navigation, source dates, backlinks |
| Coverage, citations, links, source overlap | Complete; zero coverage, link, overlap, or staged/history findings |
| Pages publishing and deployed browser check | Complete; all 296 content pages and five assets HTTP 200; live search verified |

Public site: [A Smart Bear — Unofficial Field Notes](https://kevindrafts.github.io/asmartbear-wiki/). No known blockers. Exact commands, counts, failures, tests, and deployment evidence are in the [completion report](completion.md).

## Durable checkpoints

The pilot validated complete extraction of old/new essays, mailbags, long pages, tables, diagrams, and footnotes before completing the sequential crawl. Editorial batches reached 69, 132, then 226 reviewed notes. All extracted bodies were read; notes were manually authored after reading, never from titles alone. Topic consolidation produced 43 substantive pages, followed by ten guides and five reading paths.

Final discovery corrected the initial estimates: 14 hidden mailbags, and two off-sitemap essays (`growth-asymptote`, `swot`). These two essays have future-dated source metadata (2030), retained with an explicit caveat. Twenty legacy redirect chains were checked: one included canonical alias, 19 outside the longform boundary. No canonical duplicates in the included set.

Full source HTML and bodies remain only in `/Users/mordecai/.hermes/data/jason-cohen-source-cache`. The atomic external ledger records fetch, read, review, hash, and synthesis states; public catalog exports contain metadata only. No scheduled updates.

MkDocs was selected as the approved simpler established alternative to Quartz: Markdown-first, local browser search, responsive navigation, and a small reproducible build without a vendored application.

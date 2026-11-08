# Build status

Updated November 8, 2026. The weekly update adds [E13 with Ruben Gamez and Nusii](podcast-update.md), bringing coverage to 240 reviewed sources: 227 articles/mailbags and thirteen episodes. Four topics and two guides receive changes. The new transcript was read completely; all twelve earlier transcript bodies match their reviewed hashes. Blog discovery found no new articles or changed timestamps. All 25 tests pass (22 Python and three JavaScript). The strict site build and complete-corpus, citation, link, and source-cache audits pass with 240 notes and zero errors. Staged/history review and publication verification are pending.

| Phase | State |
|---|---|
| Test-first ingestion and validators | Complete; 22 Python and three JavaScript tests pass |
| Pilot extraction/read/build | Complete; 12 varied sources, full-body tail and structure checks |
| Longform discovery and classification | Complete for the essay update; 275 URL records, 227 included, 48 exclusions |
| Longform capture and reading | Complete; 227 bodies, 344,815 extracted words, zero included fetch failures; two additional full rereadings in the October 25 update |
| Original source notes | Complete; 227 article/mailbag notes and thirteen podcast notes tied to source-body hashes |
| Podcast reading | Complete; thirteen of thirteen located transcripts reviewed, 310,359 extracted words including speaker labels and timestamps |
| Cross-article synthesis | Complete; 43 topics, 10 decision guides, five reading paths |
| Static site and search | Complete; MkDocs, responsive navigation, source dates, backlinks |
| Coverage, citations, links, source overlap | Complete; 240 reviewed notes, zero errors; 90 transcript anchors verified |
| Pages publishing and deployed-site checks | November 8 publication pending; November 1 release verified |

Public site: [A Smart Bear — Unofficial Field Notes](https://kevindrafts.github.io/asmartbear-wiki/). Exact commands, counts, failures, tests, and deployment evidence are in the [completion report](completion.md).

## Durable checkpoints

The pilot validated complete extraction of old/new essays, mailbags, long pages, tables, diagrams, and footnotes before completing the sequential crawl. Editorial batches reached 69, 132, then 226 reviewed notes. All extracted bodies were read; notes were manually authored after reading, never from titles alone. Topic consolidation produced 43 substantive pages, followed by ten guides and five reading paths.

Final discovery corrected the initial estimates: 14 hidden mailbags, and two off-sitemap essays (`growth-asymptote`, `swot`). These two essays have future-dated source metadata (2030), retained with an explicit caveat. Twenty legacy redirect chains were checked: one included canonical alias, 19 outside the longform boundary. No canonical duplicates in the included set.

Full source HTML and bodies remain only in `/Users/mordecai/.hermes/data/jason-cohen-source-cache`. The atomic external ledger records fetch, read, review, hash, and synthesis states; public catalog exports contain metadata only. The user separately authorized weekly local Codex updates for Sundays at 3 AM America/Chicago; no repository cron or scheduled source crawl was added.

MkDocs was selected as the approved simpler established alternative to Quartz: Markdown-first, local browser search, responsive navigation, and a small reproducible build without a vendored application.

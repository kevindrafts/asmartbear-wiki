# Smart Bear Live update — October 17, 2026

This batch adds five original episode notes and a [podcast reading index](../wiki/podcasts.md). The wiki now includes 232 reviewed sources: 227 articles and mailbags plus five podcast conversations. Six topic pages and three decision guides connect the new material to existing readings; totals remain 43 topics, 10 guides, and five reading paths.

## Sources and reading

| Episode | Official publication date | Extracted words | Reading and note |
|---|---|---:|---|
| [E02: DropInBlog](https://smartbearlive.transistor.fm/2/transcript) | August 16, 2026 | 34,357 | Complete; reviewed |
| [E03: Podsqueeze](https://smartbearlive.transistor.fm/3/transcript) | August 23, 2026 | 35,665 | Complete; reviewed |
| [E05: PostPlanify](https://smartbearlive.transistor.fm/5/transcript) | September 6, 2026 | 24,766 | Complete; reviewed |
| [E08: PainPointy](https://smartbearlive.transistor.fm/8/transcript) | September 27, 2026 | 15,419 | Complete; reviewed |
| [E09: DevriX](https://smartbearlive.transistor.fm/9/transcript) | October 4, 2026 | 29,872 | Complete; reviewed |

All 140,079 extracted words, including speaker labels and timestamps, were read from the full official transcript containers without a length cutoff. Long readings were split at paragraph boundaries in the external cache; truncated tool displays were reread before completing review. Each public record binds review to the exact extracted-body hash.

The official episode list showed nine episodes on the discovery date. Transcripts were located for all nine, but episodes 1, 4, 6, and 7 have not been fully reviewed. Availability is not counted as reading coverage. Publication dates come from each official episode page, not an inferred recording date.

## Editorial decisions

Notes distinguish Cohen, co-hosts, and founders; operating figures remain participant reports. Questions, hypothetical pricing, positioning, and strategic buyer stories are not reported as successful outcomes. The interview episode designs research but does not supply its results. E05 has inconsistent speaker labels and timestamp ordering; clear exchanges and joint attribution are used where appropriate. No transcript was verified against audio.

The new notes are concise commentary rather than transcripts, quotations, or a substitute for listening. Full HTML and extracted text stay only in the designated external cache. The separate `catalog/podcasts.jsonl` contains metadata and review hashes. The build and audits combine public catalogs, while blog ingestion retains its original boundary. CI needs no source fetches.

## Validation and publication

All 25 tests pass (22 Python, three JavaScript). The strict MkDocs build and complete-corpus/cache validator pass with 232 notes and zero errors. All 22 unique timestamp links used in the new commentary match links in the cached official transcript HTML. Desktop inspection, mobile navigation at 390 × 844, and search for PainPointy passed; the podcast index and E08 note had no horizontal page overflow.

The new synthetic tests were observed failing before implementation. They cover separate-catalog loading, podcast attribution metadata, official transcript URLs, pending-review rejection, and counting episodes rather than timestamp fragments as distinct sources. External-cache scanning covers all selected transcripts as well as the articles.

Staged/history review passed with zero findings. Content commit `f18a4ac` was published by [deployment 39059148772](https://github.com/kevindrafts/asmartbear-wiki/actions/runs/39059148772), which independently passed tests, validation, and the strict build. All **310 live HTTP checks passed: 305 content pages and five assets**. All 305 pages are present in search. A live browser search for DevriX opened E09 with its source links, dates, and backlinks intact.

Machine-readable results are in `reports/audit-results.json`, `reports/git-audit-results.json`, and `reports/deployment-audit.json`. This final evidence update uses the same validated publishing workflow. See [completion](completion.md) for commands and remaining scope qualifications.

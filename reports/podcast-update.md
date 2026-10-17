# Smart Bear Live update — October 17, 2026

The initial batch added five episode notes; the follow-up adds the remaining four. The wiki now includes **236 reviewed sources: 227 articles and mailbags plus all nine Smart Bear Live episodes listed on October 17, 2026**. All 245,167 extracted transcript words were read externally. The [podcast index](../wiki/podcasts.md) reaches every episode. Totals remain 43 topics, 10 guides, and five reading paths.

## Initial five-episode batch

The first batch connected five selected conversations to six topic pages and three decision guides. Its reading and publication evidence follows; the four-episode completion is recorded below.

## Sources and reading

| Episode | Official publication date | Extracted words | Reading and note |
|---|---|---:|---|
| [E02: DropInBlog](https://smartbearlive.transistor.fm/2/transcript) | August 16, 2026 | 34,357 | Complete; reviewed |
| [E03: Podsqueeze](https://smartbearlive.transistor.fm/3/transcript) | August 23, 2026 | 35,665 | Complete; reviewed |
| [E05: PostPlanify](https://smartbearlive.transistor.fm/5/transcript) | September 6, 2026 | 24,766 | Complete; reviewed |
| [E08: PainPointy](https://smartbearlive.transistor.fm/8/transcript) | September 27, 2026 | 15,419 | Complete; reviewed |
| [E09: DevriX](https://smartbearlive.transistor.fm/9/transcript) | October 4, 2026 | 29,872 | Complete; reviewed |

All 140,079 extracted words, including speaker labels and timestamps, were read from the full official transcript containers without a length cutoff. Long readings were split at paragraph boundaries in the external cache; truncated tool displays were reread before completing review. Each public record binds review to the exact extracted-body hash.

The official episode list showed nine episodes on the discovery date. At the end of the initial batch, episodes 1, 4, 6, and 7 remained unreviewed; the follow-up below completes them. Availability is not counted as reading coverage. Publication dates come from each official episode page, not an inferred recording date.

## Editorial decisions

Notes distinguish Cohen, co-hosts, and founders; operating figures remain participant reports. Questions, hypothetical pricing, positioning, and strategic buyer stories are not reported as successful outcomes. The interview episode designs research but does not supply its results. E05 has inconsistent speaker labels and timestamp ordering; clear exchanges and joint attribution are used where appropriate. No transcript was verified against audio.

The new notes are concise commentary rather than transcripts, quotations, or a substitute for listening. Full HTML and extracted text stay only in the designated external cache. The separate `catalog/podcasts.jsonl` contains metadata and review hashes. The build and audits combine public catalogs, while blog ingestion retains its original boundary. CI needs no source fetches.

## Validation and publication

All 25 tests pass (22 Python, three JavaScript). The strict MkDocs build and complete-corpus/cache validator pass with 232 notes and zero errors. All 22 unique timestamp links used in the new commentary match links in the cached official transcript HTML. Desktop inspection, mobile navigation at 390 × 844, and search for PainPointy passed; the podcast index and E08 note had no horizontal page overflow.

The new synthetic tests were observed failing before implementation. They cover separate-catalog loading, podcast attribution metadata, official transcript URLs, pending-review rejection, and counting episodes rather than timestamp fragments as distinct sources. External-cache scanning covers all selected transcripts as well as the articles.

Staged/history review passed with zero findings. Content commit `f18a4ac` was published by [deployment 39059148772](https://github.com/kevindrafts/asmartbear-wiki/actions/runs/39059148772), which independently passed tests, validation, and the strict build. All **310 live HTTP checks passed: 305 content pages and five assets**. All 305 pages are present in search. A live browser search for DevriX opened E09 with its source links, dates, and backlinks intact.

Machine-readable results are in `reports/audit-results.json`, `reports/git-audit-results.json`, and `reports/deployment-audit.json`. This final evidence update uses the same validated publishing workflow. See [completion](completion.md) for commands and remaining scope qualifications.

## Follow-up completing the listed episodes

The official [episode list](https://smartbearlive.transistor.fm/episodes) was rechecked on October 17 and still listed nine episodes. There was no exclusion rule for the remaining four: the first batch was a selected reading batch. The user's follow-up requested the rest.

| Episode | Official publication date | Extracted words | Reading and note |
|---|---|---:|---|
| [E01: ScreenshotOne](https://smartbearlive.transistor.fm/1/transcript) | July 23, 2026 | 29,498 | Complete; reviewed |
| [E04: Appointmed](https://smartbearlive.transistor.fm/4/transcript) | August 30, 2026 | 26,898 | Complete; reviewed |
| [E06: Ymir](https://smartbearlive.transistor.fm/6/transcript) | September 13, 2026 | 32,128 | Complete; reviewed |
| [E07: NaiL](https://smartbearlive.transistor.fm/7/transcript) | September 20, 2026 | 16,564 | Complete; reviewed |

All **105,088 additional extracted words**, including speaker labels and timestamps, were read in 19 paragraph-preserving chunks with no truncated displays. Notes bind to the complete extracted-body hashes. Cached source pages from the same day's discovery were reused; no source JSON or `/ref/` endpoints were requested. Full sources remain exclusively in the external cache.

Nine topic pages and three guides gain original synthesis. E01 separates temporary use from recurring demand and market discovery from scalable acquisition. E04 preserves Walling's attribution and separates personal purpose from company direction. E06 retains the shift from software alone toward implementation and training, including Adams's correction of the buyer hypothesis. E07 keeps the unresolved repeatability question and distinguishes common-parent expansion from diversification. None reports the proposed strategy as a completed result.

E04's printed timestamps have no source-provided clickable anchors. Its citations therefore link to the full transcript with text locators. E01 and E04 extend beyond the audio durations listed on their episode pages; source links are not represented as verified audio alignment. No audio review was performed.

All 25 tests pass (22 Python and three JavaScript). The strict MkDocs build and complete-corpus/cache audit pass with 236 notes and zero errors. All 41 unique timestamp links across the podcast commentary match official cached HTML, including 19 for the added episodes. Complete-container extraction checks also passed for all four new transcripts. Publication verification is pending; earlier deployment figures above describe the initial five-episode release.

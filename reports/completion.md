# Completion and publication verification

## October 17 incremental update

Added one reviewed essay and refreshed two source reviews after checking current homepage, RSS, and sitemap discovery. The collection now contains 227 notes; topic, guide, and reading-path counts are unchanged. See the [update report](recent-update.md) for scope and qualifications. All 22 tests passed (19 Python, three JavaScript), the strict build passed, and the complete coverage/cache audit reported zero errors for 227 notes. Browser checks verified the new note's source date, original-source link, backlinks, search result for `OKRs`, and mobile layout and navigation at 390 × 844. The content update was published in commit `495e2ba`; [deployment 39057570993](https://github.com/kevindrafts/asmartbear-wiki/actions/runs/39057570993) succeeded. The live-site audit passed all 303 HTTP checks (298 content pages and five assets), found all 298 pages in search, and reported zero errors. Live browser search for `OKRs` opened the new note with the correct date and source link. The evidence below the October section records the original September release.

Commands for this update:

```sh
node --test tests/search.test.cjs
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m scripts.finalize_site
.venv/bin/python -m scripts.build_site
.venv/bin/mkdocs build --strict
.venv/bin/python -m scripts.validate --require-complete --cache-audit
.venv/bin/python -m scripts.review_git --cache-audit
git diff --cached --check
.venv/bin/python -m scripts.check_deployment
```

Staged-file and existing-history audits reported zero findings. The final verification-report refresh is published through the same validated Pages workflow.

The deployment checker now derives its expected article count from the catalog, so it can reject the old 226-note homepage after this update.

## September 30 original release

**Complete — September 30, 2026.** The wiki is built, committed, pushed, and publicly deployed at [kevindrafts.github.io/asmartbear-wiki](https://kevindrafts.github.io/asmartbear-wiki/). There are no known included-source, editorial coverage, build, or deployment blockers.

## Delivered counts

| Deliverable | Verified count |
|---|---:|
| Classified discovery records | 274 |
| Included canonical sources | 226 |
| Essays / mailbags | 212 / 14 |
| Complete bodies fetched and read | 226 |
| Extracted source words, external cache only | 343,448 |
| Reviewed original article notes | 226 |
| Cross-article topic pages | 43 |
| Practical decision guides | 10 |
| Stage-based reading paths | 5 |
| Explicit exclusions | 48 |
| Included fetch failures / unread bodies / pending reviews | 0 / 0 / 0 |
| Duplicate included canonical URLs | 0 |
| Deployed content pages, excluding the custom 404 page | 296 |

The site provides source-linked Markdown, visible source dates, topic collections, backlinks, responsive navigation, client-side search, an unofficial disclaimer, attribution, and separate editorial licensing with third-party exclusions. The external ledger is resumable; public catalog exports contain metadata and hashes only. Official workshops are linked, not reproduced. No scheduled updates are configured.

## Tests and audits

The final local verification commands were:

```sh
node --test tests/search.test.cjs
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m scripts.finalize_site
.venv/bin/python -m scripts.build_site
.venv/bin/mkdocs build --strict
.venv/bin/python -m scripts.validate --require-complete --cache-audit
.venv/bin/python -m scripts.review_git --cache-audit
git diff --cached --check
.venv/bin/python -m scripts.check_deployment
```

**22 tests passed: 19 Python and three JavaScript.** Ingestion and validator tests were written before implementation; hardening and search regression tests were also observed failing before their implementation. GitHub Actions independently ran the tests, complete-corpus validator, and strict build successfully.

Coverage, note hashes and dates, canonical uniqueness, citations, synthesis references, local links and anchors, and homepage reachability passed with zero errors. All 226 reviewed hashes match the external bodies read. Source-overlap checks across editorial Markdown, rendered HTML, search entries, staged files, and existing Git blobs reported zero findings. Raw-capture and recognizable credential-pattern scans also reported zero findings. Full source articles never entered Git or the public build. See [editorial audit](editorial-audit.md) for the scope and limitations of these checks.

The deployed-site audit made **301 HTTP checks: all 296 content pages plus five search/style assets returned HTTP 200; zero failures**. It also confirmed all 296 pages were represented in the search index. Machine-readable results are stored in repository files `reports/audit-results.json`, `reports/git-audit-results.json`, and `reports/deployment-audit.json`.

## Browser acceptance

Chrome testing covered desktop and 390 × 844 mobile layouts, collapsed and expanded navigation, search input/paste, typing during search initialization, distinct page results, guide-to-note navigation, original-source links, source dates, and backlinks. A hidden mailbag note was opened from public search. No console errors were observed in the checked search flow.

Every required founder question was tested independently against the deployed site:

| Query | Verified useful result |
|---|---|
| How should I price this? | [Pricing guide](../wiki/guides/price-product.md) |
| How do I select an ICP? | [Customer-selection guide](../wiki/guides/select-customer.md) |
| What should version one include? | [First-version guide](../wiki/guides/first-version.md) |
| Why has growth stalled? | [Growth diagnosis](../wiki/guides/stalled-growth.md) |
| When should I hire? | [Hiring and management guide](../wiki/guides/hire-and-manage.md) |

Browser testing found and resolved reserved-frontmatter rendering, early search initialization, question-mark parsing, and stale browser caching of the search asset. These were repaired and retested before completion.

## Publication evidence

Repository: [kevindrafts/asmartbear-wiki](https://github.com/kevindrafts/asmartbear-wiki), public, branch `main`.

```sh
gh api --method POST repos/kevindrafts/asmartbear-wiki/pages -f build_type=workflow
git commit -m 'Build complete source-linked A Smart Bear wiki'
git push origin main
gh run watch 36734638622 --repo kevindrafts/asmartbear-wiki --exit-status --interval 10
gh run view 36735375705 --repo kevindrafts/asmartbear-wiki --json status,conclusion,url
gh run view 36735658976 --repo kevindrafts/asmartbear-wiki --json status,conclusion,url
```

- Initial complete-content commit: `3b355e6`; [deployment 36734638622](https://github.com/kevindrafts/asmartbear-wiki/actions/runs/36734638622) succeeded.
- Search regression fix: `1761c53`; [deployment 36735375705](https://github.com/kevindrafts/asmartbear-wiki/actions/runs/36735375705) succeeded, including all 22 tests.
- Browser asset versioning: `4203f14`; [deployment 36735658976](https://github.com/kevindrafts/asmartbear-wiki/actions/runs/36735658976) succeeded. All five founder questions passed on this public release.
- This final report and build-status update are published through the same validated workflow. Deployment runs remain visible in [Actions](https://github.com/kevindrafts/asmartbear-wiki/actions).

## Qualifications, not unresolved coverage failures

The publicly reachable off-sitemap essays `growth-asymptote` and `swot` carry anomalous 2030 source dates, preserved with explicit caveats. The `price-low` source omits amounts in its question; the note does not reconstruct them. Nineteen legacy destinations remain deliberately outside longform scope; one additional legacy URL aliases an included article. All 20 checked legacy chains ended in HTTP 200. Robots-excluded JSON and `/ref/` endpoints were never requested.

All bodies, footnotes, extracted table cells, alt text, and captions were read. Diagram meaning and source conflicts are preserved in original commentary; not every decorative image received pixel-level inspection. Multiple articles by one author are not independent corroboration, and third-party research cited by that author was not imported as another corpus. See [coverage](coverage.md) for the complete boundary and exclusion ledger.

## October 17 podcast batch

The counts above describe the original September release. Following the [October essay update](recent-update.md), this batch adds five reviewed Smart Bear Live conversations (episodes 2, 3, 5, 8, and 9). Coverage at that point was **232 notes: 227 articles and mailbags plus five episodes**, with 43 topics, 10 guides, and five paths. Full reading covered 140,079 extracted transcript words including speaker labels and timestamps. Nine transcripts were located; four remain outside this reviewed batch. See [podcast update](podcast-update.md).

The verification commands in the earlier test section were rerun for this batch through the strict build and cache audit. **25 tests passed: 22 Python and three JavaScript.** New synthetic tests cover podcast catalog separation, participant metadata, official transcript URLs, review status, and source identity across timestamps. The full validator reported zero errors. All 22 unique cited timestamps exist in the cached official HTML.

Local browser checks covered the podcast index, E08 source links and dates, search for PainPointy and opening its result, and mobile navigation at 390 × 844. The index and episode note fit the mobile viewport without horizontal page overflow. Transcript wording, speaker labels, and time alignment were not verified against audio; known E05 inconsistencies are documented.

Staged/history review passed with zero findings. Content commit `f18a4ac` was deployed by [run 39059148772](https://github.com/kevindrafts/asmartbear-wiki/actions/runs/39059148772), which independently passed all tests, the validator, and strict build. The deployed-site audit passed **310 HTTP checks: 305 content pages plus five assets**; all 305 content pages are indexed. The live podcast index and a DevriX search leading to E09 were verified in the browser, including source dates, transcript/audio links, and backlinks.

```sh
git commit -m 'Add five reviewed Smart Bear Live conversations and wiki connections'
git push origin main
gh run watch 39059148772 --repo kevindrafts/asmartbear-wiki --exit-status --interval 15
.venv/bin/python -m scripts.check_deployment
```

This evidence update is published through the same validated workflow. Current audit JSON files record the combined article and podcast collection. No source payloads entered Git, the site, or its search index. No scheduled updates were created.

## October 17 podcast completion follow-up

The follow-up adds episodes 1, 4, 6, and 7 after complete reading of 105,088 additional extracted words. Current coverage is **236 notes: 227 articles and mailbags plus all nine listed Smart Bear Live episodes**, totaling 245,167 podcast words including labels and timestamps. Nine topic pages and three guides gain source-linked synthesis. The official episode list was rechecked and still listed nine episodes. See [podcast update](podcast-update.md) for reading and transcript limitations.

All 25 tests, the strict build, and the complete-corpus/cache audit pass with 236 notes and zero errors. All 41 unique cited transcript anchors match the official cached HTML, including 19 for the new episodes. Complete-container extraction checks passed for all four transcripts. Content commit `c29a362` was pushed to `main` and published by [deployment 39063781826](https://github.com/kevindrafts/asmartbear-wiki/actions/runs/39063781826), which independently passed all tests, validation, and the strict build. Staged/history review reported zero findings. The live audit passed **314 HTTP checks: 309 content pages and five assets**, with all 309 pages present in search and zero errors. Browser inspection verified the nine-episode index and E04 note, including publication date, primary-source links, and backlinks. The browser retained an earlier search index immediately after deployment; a direct check confirmed the public index contains the new notes (the asset has a ten-minute cache lifetime). No successful browser search for the new episodes is claimed for this check. The earlier no-schedule statements describe their historical batches; the user has since authorized a weekly Sunday 3 AM America/Chicago task in the local Codex app.


## October 18 weekly update

Added E10 after reading the complete 17,272-word official transcript. Coverage is 237 reviewed sources (227 articles/mailbags and ten podcast episodes). The nine earlier transcripts match their reviewed body hashes. The blog homepage, feed, and sitemap revealed no new article candidates or changed sitemap timestamps; unchanged article bodies were not fetched again. Four topic pages and one guide receive original synthesis. See [podcast update](podcast-update.md) for source links, qualifications, and the external-only capture boundary.

All 25 tests pass (22 Python and three JavaScript). The strict build and complete-corpus/cache validator pass with 237 notes and zero errors. All 51 unique transcript anchors match the cached official HTML, including ten for E10. Publication verification is pending.

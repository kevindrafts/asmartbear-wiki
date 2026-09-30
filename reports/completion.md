# Completion and publication verification

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

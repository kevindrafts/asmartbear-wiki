# A Smart Bear — Unofficial Field Notes

An independent, source-linked reading companion to Jason Cohen's company-building essays.

**Website:** https://kevindrafts.github.io/asmartbear-wiki/

226 reviewed article notes, 43 cross-article topics, 10 decision guides, and five reading paths. Every included article body was read in full; original sources remain linked, not republished. The September 30, 2026 snapshot includes 14 mailbags and two essays discovered beyond the sitemap. See [coverage](reports/coverage.md), [build status](reports/build-status.md), and [completion](reports/completion.md).

## Build and check

Python 3.9 or later (CI uses 3.12). No source fetch is needed to build.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install --cache-dir .cache/pip -r requirements.txt
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m scripts.finalize_site
.venv/bin/python -m scripts.build_site
.venv/bin/python -m scripts.validate --require-complete
.venv/bin/mkdocs build --strict
.venv/bin/python -m http.server 8000 --directory site/public
```

Open http://localhost:8000/. MkDocs supplies responsive navigation and local client-side search; the staging script adds catalog views, source dates, topic collections, and backlinks. Authored Markdown remains in `processed/` and `wiki/`. Generated `site/docs/` and `site/public/` are ignored by Git. GitHub Actions builds only those public editorial inputs and deploys to Pages on pushes to `main`; it never crawls source articles.

## Source handling

Full source captures are allowed **only** in `/Users/mordecai/.hermes/data/jason-cohen-source-cache`. No raw articles, source images, or real article-body test fixtures belong in this repository, history, build, or search index. The public catalog contains metadata and review hashes only. This fixed external path is deliberate; change it only with explicit authorization.

```sh
# Resume discovery/fetch; sequential, robots-aware, >=2.1 seconds between requests.
.venv/bin/python -m scripts.ingest --limit 12
.venv/bin/python -m scripts.ingest
.venv/bin/python -m scripts.reconcile
# Additional local check requires the external source cache:
.venv/bin/python -m scripts.validate --require-complete --cache-audit
# After staging, inspect all staged files and every existing Git blob:
.venv/bin/python -m scripts.review_git --cache-audit
```

Ingestion resumes the frozen snapshot; it does not silently refresh existing cached sources. Updated source bodies require deliberate re-extraction and a new complete reading, then a matching reviewed hash. The ledger is atomic and records discovery, fetch, reading, review, and synthesis references. Editorial content is manually authored; no title-only summary generator is used. See [contributing](CONTRIBUTING.md) and [catalog schema](catalog/SCHEMA.md).

## Rights and affiliation

Unofficial; not affiliated with or endorsed by Jason Cohen, A Smart Bear, SmartBear, or WP Engine. Original project code is [MIT](LICENSE); original editorial content is [CC BY 4.0](CONTENT-LICENSE.md), with explicit third-party exclusions. Jason Cohen retains rights in the underlying articles. The [official workshops](https://skills.asmartbear.com/) are linked, not copied. No scheduled updates are configured.

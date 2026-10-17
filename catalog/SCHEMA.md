# Public catalog schema

Each line is one JSON object. The external `ledger.json` is the resumable discovery/review checkpoint; these exports contain metadata only, never article payloads.

`articles.jsonl` contains one record per included canonical article:

| Field | Meaning |
|---|---|
| `id` | Stable path-derived note ID; lowercase letters, digits, hyphens |
| `url`, `canonical_url`, optional `resolved_url` | Discovered, declared canonical, and observed redirect destination |
| `title`, `source_type`, `classification` | Source title and article/mailbag distinction |
| `discovered_via` | Sitemap, homepage, RSS, or referring article IDs; routes overlap |
| `published`, `modified` | Source article metadata timestamps; null when absent |
| `sitemap_lastmod` | Separate discovery timestamp; never substitutes for publication |
| `fetched_at` | Capture/extraction checkpoint timestamp, not publication |
| `word_count`, `image_count`, `table_count` | Completeness/structure metadata |
| `html_sha256`, `body_sha256` | Hashes of external raw HTML and full extracted body |
| `status`, `read_status`, `note_status` | Fetch, complete reading, and editorial review states |
| `reviewed_body_sha256` | Must equal current body hash for a reviewed note |
| `tags`, `synthesis_references` | Topic slugs and corresponding authored page paths |

`exclusions.jsonl` retains every discovered non-article within the source-domain boundary with its URL, discovery routes, classification, explicit exclusion reason, and applicable redirect chain/status/destination. Robots exclusions are records, not fetched endpoint bodies. Legacy aliases are classified separately without double-counting their included canonical article. Third-party external citations are not an additional recursive corpus.

Note frontmatter preserves source URL, title, author, dates, type, review status, body hash, and topics. The renderer makes source dates visible without publishing body hashes as article prose. `scripts.validate` enforces metadata matching, canonical uniqueness, review completeness, citations, link reachability, and source separation.

`podcasts.jsonl` is a separate metadata-only catalog for explicitly selected,
fully reviewed Smart Bear Live episodes. It uses the common fields above plus
integer `episode` and a nonempty `participants` list; `classification` and
`source_type` are `podcast`. `url` points to the official episode and
`canonical_url` to its `/transcript` page. `published` preserves the episode page's
date-only precision; absent modification dates remain null. Word counts include
speaker labels and timestamps in the complete extracted transcript container.
`fetched_at` is the cached HTML capture timestamp.

Its external ledger is `smartbear-live/ledger.json` inside the designated cache,
separate from blog discovery. Each reviewed external body is also stored under its
stable note ID for the common hash and overlap audits. `scripts.catalog` combines
the public catalogs for staging and validation; blog export still owns only the
article catalog. Located but unread episodes are not exported as reviewed sources.

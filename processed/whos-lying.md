---
title: Who’s lying?
source: https://longform.asmartbear.com/whos-lying/
author: Jason Cohen
published: '2022-02-26T00:00:00Z'
modified: '2025-03-03T21:11:45Z'
source_type: article
status: reviewed
source_sha256: 0c510e4d8eab3f23e70038bb9ca35fc614a8eb58a348e8c02b776b1b7e77c0a2
topics:
- metrics
- uncertainty
- technical-debt
---

# Who’s lying?

[Read Jason Cohen’s original](https://longform.asmartbear.com/whos-lying/) · Unofficial editorial note.

A plane's stuck fuel gauges lead Cohen to a lesson about business dashboards: two readings are not independent if they share the same failure mode. Billing data, bank receipts, application activity, and server logs can reveal discrepancies that one reporting pipeline hides. Reconciliation also improves understanding of what each measure actually represents.

**Apply it:** Independently recompute an important metric, document differences in definitions and timing, and investigate unexplained divergence before acting on a trend.

**Boundary:** Agreement among several sources is stronger only to the extent their errors are independent; shared instrumentation can reproduce the same mistake. Revenue and cash receipts, for example, require reconciliation rather than an expectation of equality.

Related: [Metrics](../wiki/topics/metrics.md) · [Uncertainty](../wiki/topics/uncertainty.md) · [Technical Debt](../wiki/topics/technical-debt.md)

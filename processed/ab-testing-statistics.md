---
title: Easy statistics for A/B testing and hamsters
source: https://longform.asmartbear.com/ab-testing-statistics/
author: Jason Cohen
published: '2009-04-06T08:00:00Z'
modified: '2025-07-09T02:37:15Z'
source_type: article
status: reviewed
source_sha256: 0eabd64cc62755443b3cce823ab45a9fd286e144135f1e2d5b98ed2721a03315
topics:
- experimentation
---

# Easy statistics for A/B testing and hamsters

[Read Jason Cohen’s original](https://longform.asmartbear.com/ab-testing-statistics/) · Unofficial editorial note.

Cohen uses a small click-count example and a hamster’s food choices to show why a large-looking ratio can still be inconclusive. His table contrasts the same proportional difference at different sample sizes, and his appendix derives a simplified chi-square threshold. The practical lesson is that limited traffic favors testing substantially different propositions over tiny cosmetic changes.

**Apply it:** Plan a comparison around an effect large enough to detect with available observations, and retain the underlying counts rather than relying on a winner badge.

**Boundary:** Editorial qualification: The derivation assumes independent categorical observations with equal expected counts under the null. It should not be generalized to unequal exposure, arbitrary conversion-rate experiments, repeated peeking, or multiple comparisons without an appropriate statistical design. A non-significant result does not by itself prove equivalence.

Related: [Experimentation](../wiki/topics/experimentation.md)

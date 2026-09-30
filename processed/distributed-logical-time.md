---
title: Distributed Logical Time
source: https://longform.asmartbear.com/distributed-logical-time/
author: Jason Cohen
published: '2019-02-23T00:00:00Z'
modified: '2025-03-03T21:02:33Z'
source_type: article
status: reviewed
source_sha256: 89887fe05abea65e556b3f9e764f1b28c9313b6d15f64630a59c4c22a6826397
topics:
- technical-debt
---

# Distributed Logical Time

[Read Jason Cohen’s original](https://longform.asmartbear.com/distributed-logical-time/) · Unofficial editorial note.

This technical essay extends a hybrid logical clock with estimated forward skew so replicas can better order events despite differing physical clocks. Counters ensure local monotonicity; receiving a peer timestamp advances local state. The diagrams distinguish causal ordering from the harder problem of ordering separate events by real time.

**Apply it:** Follow the linked implementation and paper for details; this wiki does not reproduce code.

**Boundary:** Global uniqueness is not provided, startup synchronization matters, and timestamps need not stay near real time. The claimed small ordering-error window depends on communication-delay behavior described in the article; this note is not an independent correctness proof.

Related: [Technical Debt](../wiki/topics/technical-debt.md)

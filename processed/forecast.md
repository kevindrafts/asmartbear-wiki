---
title: How to measure the accuracy of forecasts
source: https://longform.asmartbear.com/forecast/
author: Jason Cohen
published: '2016-06-28T00:00:00Z'
modified: '2025-12-06T22:05:50Z'
source_type: article
status: reviewed
source_sha256: f7e451cc2a37695390252db63287f9f92965e53225e1c97bc3a4b263e6f09171
topics:
- forecasting
- metrics
---

# How to measure the accuracy of forecasts

[Read Jason Cohen’s original](https://longform.asmartbear.com/forecast/) · Unofficial editorial note.

A probabilistic forecast needs repeated outcomes for evaluation. Cohen separates calibration—whether events occur at the predicted frequency—from useful discrimination between cases. Always predicting the base rate can be calibrated yet unhelpful. His tables develop a weighted decomposition into calibration error, resolution, and the uncertainty available in the population, corresponding to the Brier-score framework.

**Apply it:** Save predictions before outcomes occur, compare them against a base-rate baseline, and inspect both calibration and discrimination.

**Boundary:** Buckets need enough observations. The article's illustrative numbers contain inconsistencies, including the percentage rendering of five days out of 365; use independently checked calculations rather than copying its worked tables into production.

Related: [Forecasting](../wiki/topics/forecasting.md) · [Metrics](../wiki/topics/metrics.md)

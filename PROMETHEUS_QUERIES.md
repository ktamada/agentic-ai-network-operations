# Useful PromQL

```promql
sum by (source, status) (agentic_ai_incidents_total)
```

```promql
histogram_quantile(
  0.95,
  sum by (le) (rate(agentic_ai_workflow_seconds_bucket[5m]))
)
```

```promql
telco_network_path_utilization_percent{region="RDU-01"}
```

```promql
telco_network_path_utilization_percent >= 85
```

```promql
telco_network_latency_ms > 35
```

```promql
telco_network_packet_loss_percent > 1
```

```promql
(telco_network_recent_complaints / telco_network_baseline_complaints) >= 3
```

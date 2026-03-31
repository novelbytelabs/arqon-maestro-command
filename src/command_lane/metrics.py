def compute_p95(latencies_ms: list[int]) -> float:
    if not latencies_ms:
        return 0.0
    values = sorted(latencies_ms)
    idx = int(0.95 * (len(values) - 1))
    return float(values[idx])


def within_bp001_budget(latencies_ms: list[int], target_ms: int = 200) -> bool:
    return compute_p95(latencies_ms) < float(target_ms)

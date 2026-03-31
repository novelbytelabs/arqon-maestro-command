# Canary Rollout Runbook

1. Deploy to canary shard only.
2. Verify command-lane safety and latency signals for 15 minutes.
3. Validate false-positive rate gate and evidence schema gate.
4. Promote to full rollout only if all gates pass.
5. Trigger rollback drill if any safety gate fails.

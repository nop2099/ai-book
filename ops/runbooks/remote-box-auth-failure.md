# Runbook: Remote Box Auth Failure

## Symptom

- SSH returns `Permission denied`
- The target is known but batch-mode access fails

## Diagnosis

1. Confirm which user failed
2. Confirm whether the key or password path changed
3. Check whether the box should still allow that user

## Fix

1. Reconfirm the intended login path
2. Update the key, agent, or wrapper script as needed
3. Re-run the reachability check
4. If root access is no longer needed, downgrade the box in the inventory

## Escalation

- If access was intentionally removed, update the inventory and stop treating it as a live path

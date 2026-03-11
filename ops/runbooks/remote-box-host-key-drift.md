# Runbook: Remote Box Host Key Drift

## Symptom

- SSH reports `REMOTE HOST IDENTIFICATION HAS CHANGED`
- The box cannot be reached in batch mode

## Diagnosis

1. Identify the offending host and line in `~/.ssh/known_hosts`
2. Confirm whether the box was rebuilt or its SSH host keys rotated
3. Compare the new fingerprint against a trusted source before trusting it

## Fix

1. Verify the new fingerprint out of band
2. Remove the stale known-host entry
3. Reconnect and accept the new host key only after verification
4. Re-run the wall ETL inventory check

## Escalation

- If you cannot verify the new fingerprint, treat it as a trust incident and do not reconnect blindly

# Runbook: Remote Box Timeout

## Symptom

- SSH times out with no prompt

## Diagnosis

1. Confirm whether the hostname still resolves
2. Check whether the box is online in Tailscale or at its public endpoint
3. Check whether the network path changed

## Fix

1. Retry reachability from the current network
2. Verify Tailscale status or DNS resolution
3. If the box moved, update the alias and inventory
4. Re-run the ETL check after restoring connectivity

## Escalation

- If the box is expected to be online and stays dark, create an incident and surface it in the morning briefing

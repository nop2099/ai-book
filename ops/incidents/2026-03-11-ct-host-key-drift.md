# Incident: CT Host Key Drift

Date: 2026-03-11

## Summary

`ct` and `ctbd` both failed because `173.249.56.193` reported a changed host key.

## Impact

- Batch-mode wall ETL cannot read that box
- Root and nop access paths are both blocked until trust is re-established

## Next step

- Verify the new host fingerprint before updating local trust

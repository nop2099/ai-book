# Flywheel Metrics

Generated: 2026-03-11

These are starter metrics. Keep only the ones that stay useful.

## Infrastructure

- Explicit boxes discovered: 6
- Reachable boxes on latest scrape: 2
- Boxes blocked by auth or trust issues: 3
- Boxes unreachable: 1

## Candidate recurring metrics

- Host key drift incidents per month
- Remote boxes with readable `~/.claude/projects`
- Remote boxes with shell access but incomplete wall access
- Box scrape success rate
- Days since each box was last reachable

## Rules

- Add a metric only after it shows up in real observations.
- Remove a metric if it stops changing or stops driving action.
- Prefer counts and rates over vague adjectives.

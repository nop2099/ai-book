# Maintenance Inventory

Generated: 2026-03-11

## Important

### Wall ETL launch agent

- What it does: refreshes local and remote wall assets on a timer
- Owner: James
- Access: `~/Library/LaunchAgents/com.jameswilson.wall-etl.plist`
- Health check: `launchctl print gui/$(id -u)/com.jameswilson.wall-etl`

### Kai box (`ck`)

- What it does: remote shell and Claude-history source
- Owner: James
- Access: `ssh -o BatchMode=yes -o ConnectTimeout=8 kai@217.77.0.36`
- Health check: `ssh -o BatchMode=yes -o ConnectTimeout=8 kai@217.77.0.36 'echo ok'`

### Contabo nop (`contabo-nop`)

- What it does: remote shell residue source
- Owner: James
- Access: `ssh -o BatchMode=yes -o ConnectTimeout=8 nop@217.77.0.36`
- Health check: `ssh -o BatchMode=yes -o ConnectTimeout=8 nop@217.77.0.36 'echo ok'`

### CT host trust (`ct`, `ctbd`)

- What it does: remote root and nop access for `173.249.56.193`
- Owner: James
- Access: `ssh -o BatchMode=yes -o ConnectTimeout=8 root@173.249.56.193`
- Health check: `ssh -o BatchMode=yes -o ConnectTimeout=8 root@173.249.56.193 'echo ok'`

### DGX (`dgx`)

- What it does: remote Tailscale box access
- Owner: James
- Access: `ssh -o BatchMode=yes -o ConnectTimeout=8 nop@dgx.mahi-tilapia.ts.net`
- Health check: `ssh -o BatchMode=yes -o ConnectTimeout=8 nop@dgx.mahi-tilapia.ts.net 'echo ok'`

### Contabo root (`contabo`)

- What it does: root-level access path for `217.77.0.36`
- Owner: James
- Access: `ssh -o BatchMode=yes -o ConnectTimeout=8 root@217.77.0.36`
- Health check: `ssh -o BatchMode=yes -o ConnectTimeout=8 root@217.77.0.36 'echo ok'`

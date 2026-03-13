# Preflight

Check system resources before running heavy workloads. Run this before any GPU/ML inference, large builds, or memory-intensive operations.

## When To Use

- Before TTS generation, voice casting, or any ML model loading
- Before large builds or compilations
- Any time a previous run crashed due to resource exhaustion
- Proactively, when you're about to do something that needs significant disk or RAM

## Checks

Run all checks and report a go/no-go summary.

### 1. Disk Space

```bash
df -h / | awk 'NR==2 {print "Disk: " $4 " free of " $2 " (" $5 " used)"}'
```

Thresholds:
- **GO**: > 10 GB free
- **CAUTION**: 5–10 GB free — warn the user, suggest cleanup
- **NO-GO**: < 5 GB free — do not proceed with heavy workloads

### 2. Available RAM

```bash
python3 -c "
import subprocess, re
vm = subprocess.check_output(['vm_stat']).decode()
ps = 16384
free = int(re.search(r'Pages free:\s+(\d+)', vm).group(1))
inactive = int(re.search(r'Pages inactive:\s+(\d+)', vm).group(1))
spec = int(re.search(r'Pages speculative:\s+(\d+)', vm).group(1))
active = int(re.search(r'Pages active:\s+(\d+)', vm).group(1))
wired = int(re.search(r'Pages wired down:\s+(\d+)', vm).group(1))
total = 16  # GB, hardcoded for this machine
avail = (free + inactive + spec) * ps / 1024**3
used = (active + wired) * ps / 1024**3
print(f'RAM: {avail:.1f} GB available, {used:.1f} GB used, {total} GB total')
"
```

Thresholds:
- **GO**: > 8 GB available
- **CAUTION**: 4–8 GB available — small models only, warn before large ones
- **NO-GO**: < 4 GB available — do not load ML models. Suggest closing apps or using a remote machine.

### 3. GPU / Accelerator

```bash
python3 -c "
import torch
if torch.cuda.is_available():
    for i in range(torch.cuda.device_count()):
        t = torch.cuda.get_device_properties(i).total_mem / 1024**3
        f = (torch.cuda.get_device_properties(i).total_mem - torch.cuda.memory_allocated(i)) / 1024**3
        print(f'CUDA {i}: {f:.1f} GB free of {t:.1f} GB')
elif torch.backends.mps.is_available():
    print('MPS available (shares system RAM — see RAM check above)')
else:
    print('No GPU — CPU only')
" 2>/dev/null || echo "PyTorch not available in system Python — check venv"
```

For MPS (Apple Silicon): GPU memory = system RAM, so the RAM check is the GPU check. Models over ~6 GB parameters will need > 8 GB available.

### 4. Swap Pressure (optional, macOS)

```bash
sysctl vm.swapusage 2>/dev/null | awk '{print "Swap: " $0}'
```

If swap used > 2 GB, the system is already under memory pressure. Warn before adding more.

## Model Size Reference

Quick estimates for models commonly used in this project:

| Model | Parameters | ~RAM Needed (float32) | ~RAM Needed (float16) |
|---|---|---|---|
| Qwen3-TTS 0.6B Base | 0.6B | ~3 GB | ~2 GB |
| Qwen3-TTS 1.7B VoiceDesign | 1.7B | ~8 GB | ~4 GB |

## Report Format

After running all checks, output a summary like:

```
Preflight: GO / CAUTION / NO-GO

  Disk:  15 GB free (GO)
  RAM:   4.5 GB available (CAUTION — small models only)
  GPU:   MPS (shares RAM)
  Swap:  0.5 GB used (OK)

Recommendation: [what to do or not do]
```

If NO-GO on any critical check, suggest alternatives:
- Close heavy apps (browsers, Docker, etc.)
- Use a remote machine (DGX for CUDA workloads)
- Reduce model size (use 0.6B instead of 1.7B)
- Free disk space

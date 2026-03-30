#!/usr/bin/env bash
set -euo pipefail

./ops/helios/helios-run.sh python - <<'PY'
import torch

print('torch', torch.__version__)
print('cuda_available', torch.cuda.is_available())
print('torch_cuda', torch.version.cuda)

if not torch.cuda.is_available():
    raise SystemExit('FAIL: CUDA is not available')

cudnn_ver = torch.backends.cudnn.version()
print('cudnn', cudnn_ver)

x = torch.randn(1024, 1024, device='cuda', dtype=torch.float32)
y = torch.mm(x, x)
print('matmul_ok', tuple(y.shape), y.dtype)

# Basic conv to force cudnn path.
conv = torch.nn.Conv2d(3, 8, kernel_size=3, stride=1, padding=1).cuda().eval()
img = torch.randn(1, 3, 224, 224, device='cuda', dtype=torch.float32)
out = conv(img)
print('conv_ok', tuple(out.shape), out.dtype)

print('PASS: runtime hygiene gate')
PY

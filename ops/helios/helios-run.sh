#!/usr/bin/env bash
set -euo pipefail

ENV_NAME="helios-gpu-118"
CONDA_BASE="$(conda info --base)"
CONDA_PREFIX="$CONDA_BASE/envs/$ENV_NAME"

PY_SITE="$CONDA_PREFIX/lib/python3.10/site-packages"
CUDNN_LIB="$PY_SITE/nvidia/cudnn/lib"
CUDA_RUNTIME_LIB="$PY_SITE/nvidia/cuda_runtime/lib"
CUDA_NVRTC_LIB="$PY_SITE/nvidia/cuda_nvrtc/lib"
TORCH_LIB="$PY_SITE/torch/lib"

parts=()
for p in "$CUDNN_LIB" "$CUDA_RUNTIME_LIB" "$CUDA_NVRTC_LIB" "$TORCH_LIB" "$CONDA_PREFIX/lib"; do
  if [[ -d "$p" ]]; then
    parts+=("$p")
  fi
done

SANITIZED_LD="$(IFS=:; echo "${parts[*]}")"

if [[ $# -eq 0 ]]; then
  echo "Usage: $0 <command> [args...]" >&2
  exit 2
fi

exec conda run -n "$ENV_NAME" env LD_LIBRARY_PATH="$SANITIZED_LD" "$@"

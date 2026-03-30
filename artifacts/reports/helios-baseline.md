# Helios Baseline Snapshot

Captured: 2026-03-30T20:46:19Z

## System
```text
Mon Mar 30 16:46:19 2026       
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 535.288.01             Driver Version: 535.288.01   CUDA Version: 12.2     |
|-----------------------------------------+----------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
|                                         |                      |               MIG M. |
|=========================================+======================+======================|
|   0  NVIDIA GeForce RTX 2060        On  | 00000000:03:00.0  On |                  N/A |
| 26%   51C    P3              32W / 160W |   1322MiB /  6144MiB |     35%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+
                                                                                         
+---------------------------------------------------------------------------------------+
| Processes:                                                                            |
```

## Conda Environment
```text

# conda environments:
#
base                   /home/irbsurfer/miniconda3
ANE                    /home/irbsurfer/miniconda3/envs/ANE
AutoGrokML             /home/irbsurfer/miniconda3/envs/AutoGrokML
CliniAdapt-Dx          /home/irbsurfer/miniconda3/envs/CliniAdapt-Dx
Novyte_Docs            /home/irbsurfer/miniconda3/envs/Novyte_Docs
QHorizon-QNE-H-Dx      /home/irbsurfer/miniconda3/envs/QHorizon-QNE-H-Dx
arqon-maestro-asr-train   /home/irbsurfer/miniconda3/envs/arqon-maestro-asr-train
graph-regression-alt   /home/irbsurfer/miniconda3/envs/graph-regression-alt
helios-gpu-118         /home/irbsurfer/miniconda3/envs/helios-gpu-118
transformers-notebook   /home/irbsurfer/miniconda3/envs/transformers-notebook

```

## Core Toolchain
```text
rustc 1.93.0 (254b59607 2026-01-19)
cargo 1.93.0 (083ac5135 2025-12-15)
Python 3.10.19

libprotoc 29.3

pip 26.0.1 from /home/irbsurfer/miniconda3/envs/helios-gpu-118/lib/python3.10/site-packages/pip (python 3.10)

```

## Core Python Package Pins
```text
numpy 2.2.5
torch 2.10.0+cu128
protobuf 4.25.8

```

## Runtime Library Path
```text
/home/irbsurfer/miniconda3/envs/helios-gpu-118/lib/python3.10/site-packages/nvidia/cudnn/lib:/home/irbsurfer/miniconda3/envs/helios-gpu-118/lib/python3.10/site-packages/nvidia/cuda_runtime/lib:/home/irbsurfer/miniconda3/envs/helios-gpu-118/lib/python3.10/site-packages/nvidia/cuda_nvrtc/lib:/home/irbsurfer/miniconda3/envs/helios-gpu-118/lib/python3.10/site-packages/torch/lib:/home/irbsurfer/miniconda3/envs/helios-gpu-118/lib

```

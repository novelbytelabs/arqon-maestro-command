#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PROTO_DIR="$ROOT_DIR/ops/helios/contracts"
OUT_DIR="$ROOT_DIR/ops/helios/generated"
DESC_OUT="$OUT_DIR/command_contracts.desc"

mkdir -p "$OUT_DIR"

rm -f "$OUT_DIR"/command_contracts_pb2.py "$OUT_DIR"/command_contracts_pb2.pyc

./ops/helios/helios-run.sh protoc \
  --proto_path="$PROTO_DIR" \
  --descriptor_set_out="$DESC_OUT" \
  --include_imports \
  "$PROTO_DIR/command_contracts.proto"

echo "PASS: generated protobuf descriptor: $DESC_OUT"

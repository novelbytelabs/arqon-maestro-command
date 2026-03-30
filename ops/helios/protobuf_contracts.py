#!/usr/bin/env python3
from pathlib import Path

from google.protobuf import descriptor_pb2, descriptor_pool, message_factory

DESC_PATH = Path("ops/helios/generated/command_contracts.desc")
PACKAGE = "arqon.maestro.command.v1"


def _message_class(pool: descriptor_pool.DescriptorPool, full_name: str):
    descriptor = pool.FindMessageTypeByName(full_name)
    if hasattr(message_factory, "GetMessageClass"):
        return message_factory.GetMessageClass(descriptor)
    return message_factory.MessageFactory(pool).GetPrototype(descriptor)


def load_contract_classes(desc_path: Path = DESC_PATH):
    if not desc_path.exists():
        raise FileNotFoundError(
            f"Protobuf descriptor not found: {desc_path}. Run ops/helios/generate_contracts.sh"
        )

    fd_set = descriptor_pb2.FileDescriptorSet()
    fd_set.ParseFromString(desc_path.read_bytes())

    pool = descriptor_pool.DescriptorPool()
    for file_descriptor in fd_set.file:
        pool.Add(file_descriptor)

    return {
        "SpeechResult": _message_class(pool, f"{PACKAGE}.SpeechResult"),
        "CommandResult": _message_class(pool, f"{PACKAGE}.CommandResult"),
        "EvidencePacket": _message_class(pool, f"{PACKAGE}.EvidencePacket"),
        "Intent": _message_class(pool, f"{PACKAGE}.Intent"),
        "PolicyDecision": _message_class(pool, f"{PACKAGE}.PolicyDecision"),
    }

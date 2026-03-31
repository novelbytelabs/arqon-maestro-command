from src.command_lane.errors import FailClosedError


def enforce_machine_protocol(content_type: str) -> None:
    normalized = content_type.strip().lower()
    if normalized == "application/json":
        raise FailClosedError("json_machine_path_rejected")
    if normalized != "application/protobuf":
        raise FailClosedError(f"unsupported_machine_protocol:{content_type}")

from datetime import datetime


class ValidationError(ValueError):
    pass


REQUIRED_FIELDS = ["device_id", "timestamp", "latency_ms", "packet_loss", "rssi"]


def validate_metric(payload: dict) -> dict:
    for field in REQUIRED_FIELDS:
        if field not in payload:
            raise ValidationError(f"Missing field: {field}")

    device_id = str(payload["device_id"]).strip()
    timestamp = str(payload["timestamp"]).strip()
    latency_ms = _to_float(payload["latency_ms"], "latency_ms")
    packet_loss = _to_float(payload["packet_loss"], "packet_loss")
    rssi = _to_float(payload["rssi"], "rssi")

    if not device_id:
        raise ValidationError("device_id cannot be empty")

    if not timestamp:
        raise ValidationError("timestamp cannot be empty")

    _validate_timestamp(timestamp)

    if latency_ms < 0:
        raise ValidationError("latency_ms cannot be negative")

    if packet_loss < 0 or packet_loss > 100:
        raise ValidationError("packet_loss must be between 0 and 100")

    if rssi < -120 or rssi > 0:
        raise ValidationError("rssi must be between -120 and 0")

    return {
        "device_id": device_id,
        "timestamp": timestamp,
        "latency_ms": latency_ms,
        "packet_loss": packet_loss,
        "rssi": rssi,
    }


def _to_float(value, field_name: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValidationError(f"{field_name} must be a number")


def _validate_timestamp(timestamp: str) -> None:
    try:
        datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        raise ValidationError("timestamp must be valid ISO-8601 format")
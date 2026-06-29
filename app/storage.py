from decimal import Decimal
import os

import boto3


TABLE_NAME = os.getenv("METRICS_TABLE_NAME", "NetworkMetrics")


def save_metric_to_dynamodb(metric: dict, anomalies: list[str]) -> None:
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(TABLE_NAME)

    item = {
        "device_id": metric["device_id"],
        "timestamp": metric["timestamp"],
        "latency_ms": Decimal(str(metric["latency_ms"])),
        "packet_loss": Decimal(str(metric["packet_loss"])),
        "rssi": Decimal(str(metric["rssi"])),
        "is_anomaly": len(anomalies) > 0,
        "anomalies": anomalies,
    }

    table.put_item(Item=item)
import json

from app.anomaly_detector import detect_anomalies
from app.storage import save_metric_to_dynamodb
from app.validation import ValidationError, validate_metric


def lambda_handler(event, context):
    try:
        payload = _extract_payload(event)
        metric = validate_metric(payload)
        anomalies = detect_anomalies(metric)

        save_metric_to_dynamodb(metric, anomalies)

        return response(200, {
            "message": "metric accepted",
            "device_id": metric["device_id"],
            "is_anomaly": len(anomalies) > 0,
            "anomalies": anomalies,
        })

    except ValidationError as error:
        return response(400, {"message": str(error)})

    except json.JSONDecodeError:
        return response(400, {"message": "Invalid JSON body"})

    except Exception as error:
        return response(500, {"message": f"Internal error: {str(error)}"})


def _extract_payload(event):
    if "body" not in event:
        return event

    if isinstance(event["body"], dict):
        return event["body"]

    return json.loads(event["body"])


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }
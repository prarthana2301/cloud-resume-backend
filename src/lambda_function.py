import json
import os

import boto3

TABLE_NAME = os.environ.get("TABLE_NAME", "visitor-count")


def get_table():
    return boto3.resource("dynamodb").Table(TABLE_NAME)


def lambda_handler(event, context):
    response = get_table().update_item(
        Key={"id": "visits"},
        UpdateExpression="ADD #c :inc",
        ExpressionAttributeNames={"#c": "count"},
        ExpressionAttributeValues={":inc": 1},
        ReturnValues="UPDATED_NEW",
    )
    count = int(response["Attributes"]["count"])
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"count": count}),
    }
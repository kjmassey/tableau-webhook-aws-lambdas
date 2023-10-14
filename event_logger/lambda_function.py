import json
from .helpers import insert_event_record


def lambda_handler(event, context):
    try:
        insert_event_record(json.loads(event["body"]))

    except Exception as e:
        print("---- ERROR: ", str(e))

    return {"statusCode": 200, "body": json.dumps("Record Added!")}

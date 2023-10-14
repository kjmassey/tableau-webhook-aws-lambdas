import json
from .send_email import send_failure_email
from .helper import get_additional_event_details

def lambda_handler(event, context):
    event = json.loads(event.get('body'))

    augmented_resp = get_additional_event_details(event)
    send_failure_email(augmented_resp)

    return {"statusCode": 200, "body": json.dumps("Notification Sent!")}

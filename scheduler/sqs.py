import boto3
from .settings import settings
from .date_utils import date_handler
from decimal import Decimal
import json


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        # if passed in object is instance of Decimal
        # convert it to a string
        if isinstance(obj, Decimal):
            return str(obj)
        # otherwise use the default behavior
        return json.JSONEncoder.default(self, obj)


class SQSHandler:
    def __init__(self) -> None:
        self.client = boto3.client("sqs", region_name=settings.REGION_NAME)

    def schedule_event(self, event):
        """
        event must have `date`
        Args:
            event (Dict): _description_
        """
        date_to_publish = date_handler.from_isoformat(event["date"])
        seconds = date_handler.seconds_until_date(date_to_publish)

        sqs_message = {
            "MessageBody": json.dumps(
                {**event, "now": date_handler.to_isoformat(date_handler.now)},
                cls=DecimalEncoder,
            ),
            "DelaySeconds": seconds if seconds > 0 else 0,
        }
        self.client.send_message(QueueUrl=settings.QUEUE_URL, **sqs_message)
        print("Published event to queue")  # TODO change for logger

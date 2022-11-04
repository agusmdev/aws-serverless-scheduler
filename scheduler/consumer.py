from .date_utils import date_handler
from .settings import settings
from .sqs import SQSHandler
from .dynamo import DynamoDBEvents


class EventConsumer:
    def __init__(self) -> None:
        self.sqs = SQSHandler()
        self.db = DynamoDBEvents()

    def save_event(self, event):
        self.db.put_event(event)

    def publish_to_queue(self, event):
        self.sqs.schedule_event(event)

    def process_events(self, events):
        for event in events:
            date = date_handler.from_isoformat(event["date"])
            if date_handler.seconds_until_date(date) <= settings.PUBLISH_SECONDS_THRESHOLD: # Publish event to queue
                self.publish_to_queue(event)
            else:
                self.save_event(event)
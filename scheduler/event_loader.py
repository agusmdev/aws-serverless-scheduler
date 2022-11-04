from .dynamo import DynamoDBEvents
from .sqs import SQSHandler
from .date_utils import date_handler
from .settings import settings


class EventLoader:
    def __init__(self) -> None:
        self.db = DynamoDBEvents()
        self.sqs = SQSHandler()

    def publish_event(self, event):
        self.sqs.schedule_event(event)

    def publish_events(self, events):
        for event in events:
            self.publish_event(event)

    def load_events(self):
        current_segment = date_handler.get_current_segment(extra_minutes=settings.LOADER_MINUTES_THRESHOLD)
        for page in self.db.get_segment_events(current_segment):
            self.publish_events(page.get("Items", []))

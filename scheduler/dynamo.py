import boto3
from boto3.dynamodb.conditions import Key
from datetime import timedelta
from uuid import uuid4
from .settings import settings
from .date_utils import date_handler


class DynamoDBEvents:
    def __init__(self) -> None:
        self.table = boto3.resource('dynamodb', region_name=settings.REGION_NAME).Table(settings.EVENTS_TABLE)

    def get_segment_events(self, segment):
        return self.table.meta.client.get_paginator("query").paginate(
            TableName=self.table.name,
            KeyConditionExpression=Key('segment').eq(segment)
        )

    def put_event(self, event):
        date = date_handler.from_isoformat(event["date"])
        segment = date_handler.get_segment(date, extra_minutes=0)
        event_id = f"{int(date.timestamp() * 1000)}_{uuid4().hex}"
        scheduled_event = {
            **event,
            "event_id": event_id,
            "segment": segment,
            "time_to_live": int((date + timedelta(days=1)).timestamp())
        }
        print(f"Saving event! {event_id=}")
        self.table.put_item(Item=scheduled_event)
import json
import requests
from pydantic import BaseModel

# class Methods(str, Enum):
#     ...


class Event(BaseModel):
    date: str = None
    payload: dict = {}
    headers: dict = {}
    cookies: dict = {}
    method: str
    url: str


class EventEmitter:

    @staticmethod
    def send_message(event):
        requests.request(
            url=event.url,
            method=event.method,
            headers=event.headers,
            cookies=event.cookies,
            json=event.payload,
        )

    def emit_event(self, event):
        event = Event(**json.loads(event["body"]))
        self.send_message(event)
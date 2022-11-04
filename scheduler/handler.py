import json
from .consumer import EventConsumer
from .event_loader import EventLoader
from .emitter import EventEmitter

event_consumer = EventConsumer()
event_emitter = EventEmitter()
event_loader = EventLoader()

def consumer_handler(messages, _): # Messages from SNS
    events = [json.loads(ev["Sns"]["Message"]) for ev in messages["Records"]]
    event_consumer.process_events(events)

def emitter_handler(messages, _): # Events from SQS
    for event in messages["Records"]:
        event_emitter.emit_event(event)

def event_loader_handler(*_):
    event_loader.load_events()

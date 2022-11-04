from pydantic import BaseSettings


class AWSSettings(BaseSettings):
    REGION_NAME: str = "us-east-2"

class Services(BaseSettings):
    INPUT_TOPIC: str = "serverless-scheduler-input-topic"
    SQS_DELIVERY: str = "serverless-scheduler-delivery"
    EVENTS_TABLE: str = "serverless-scheduler-events"
    QUEUE_URL: str = None

class CommonSettings(BaseSettings):
    LOADER_MINUTES_THRESHOLD: int = 10 # This should be between 3 and 10
    PUBLISH_SECONDS_THRESHOLD: int = (LOADER_MINUTES_THRESHOLD + 5) * 60 # This should be 5 minutes greater than the LOADER


class Settings(Services, AWSSettings, CommonSettings): ...

settings = Settings()

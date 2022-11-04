import boto3
from scheduler.settings import settings

def init_db():
    db_client = boto3.client('dynamodb', region_name=settings.REGION_NAME)
    name = settings.EVENTS_TABLE
    if name in db_client.list_tables()['TableNames']:
        print("Table already created...")
        return

    db_client.create_table(
        TableName=name,
        AttributeDefinitions=[
            {
                'AttributeName': 'segment',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'event_id',
                'AttributeType': 'S'
            }
        ],
        KeySchema=[
            {
                'AttributeName': 'segment',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'event_id',
                'KeyType': 'RANGE'
            }
        ],
        BillingMode='PAY_PER_REQUEST',
    )
    print(f'Creating table ...')
    db_client.get_waiter('table_exists').wait(TableName=name)
    db_client.update_time_to_live(
        TableName=name,
        TimeToLiveSpecification={
            'Enabled': True,
            'AttributeName': 'time_to_live'
        }
    )
    print(f'New table {name} created!')


def init_queue():
    sqs_client = boto3.client('sqs', region_name=settings.REGION_NAME)
    name = settings.SQS_DELIVERY
    print(f'Creating queue {name}')
    create_response = sqs_client.create_queue(
        QueueName=name,
    )
    url = create_response['QueueUrl']
    print(f'Created topic {name} with arn {url}')

def init_input_topic():
    sns_client = boto3.client('sns', region_name=settings.REGION_NAME)
    name = settings.INPUT_TOPIC
    print(f'Creating topic {name}')
    create_response = sns_client.create_topic(
        Name=name,
    )

    arn = create_response['TopicArn']
    print(f'Created topic {name} with arn {arn}')


if __name__ == '__main__':
    init_db()
    init_queue()
    init_input_topic()
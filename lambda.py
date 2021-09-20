from __future__ import print_function
import json
import base64
import boto3

def lambda_handler(event, context):
    # Reading from Kinesis
    messages = []
    for record in event['Records']:
        # Kinesis data is base64 encoded so decode here
        payload = base64.b64decode(record["kinesis"]["data"])
        print("Decoded payload: " + str(payload))
        try:
            message = json.loads(payload)
            message["errors"] = message["message"].split().count('error')
            message["id"] = int(message["id"])
            messages = messages + [message]
        except:
            print(f'Kinesis Data: {record["kinesis"]["data"]}\nSomething went wrong, not processing record...\n')

    # Writing into DynamoDB table dynamodb-kinesis
    client = boto3.resource('dynamodb')
    table = client.Table("dynamodb-kinesis")
    for message in messages:
        table.put_item(Item=message)

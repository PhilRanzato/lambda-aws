from __future__ import print_function
import json
import base64
import boto3


def lambda_handler(event, context):
    print('Reading from kinesis...\n')

    messages = []

    for record in event['Records']:
        # Kinesis data is base64 encoded so decode here
        payload = base64.b64decode(record["kinesis"]["data"])
        print("Decoded payload: " + str(payload))

        message = json.loads(payload)
        message["errors"] = message["message"].split().count('error')
        message["id"] = int(message["id"])

        messages = messages + [message]

    print("writing into dynamodb...\n")

    client = boto3.resource('dynamodb')

    table = client.Table("dynamodb-kinesis")
    #  print(table.table_status)

    for message in messages:
        print(message)
        print(message["id"])
        # message["part_key"] = "part_key"
        table.put_item(Item=message)

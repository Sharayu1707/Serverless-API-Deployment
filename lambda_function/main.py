import json
import boto3
import uuid

table = boto3.resource('dynamodb').Table('serverless-items')

def lambda_handler(event, context):
    method = event['httpMethod']

    if method == 'POST':
        body = json.loads(event['body'])
        item = {
            "id": str(uuid.uuid4()),
            "name": body['name']
        }
        table.put_item(Item=item)
        return respond(200, item)

    elif method == 'GET':
        result = table.scan()
        return respond(200, result['Items'])

    elif method == 'PUT':
        body = json.loads(event['body'])
        table.update_item(
            Key={"id": body['id']},
            UpdateExpression="SET #n = :name",
            ExpressionAttributeNames={"#n": "name"},
            ExpressionAttributeValues={":name": body['name']}
        )
        return respond(200, {"message": "Item updated"})

    elif method == 'DELETE':
        body = json.loads(event['body'])
        table.delete_item(Key={"id": body['id']})
        return respond(200, {"message": "Item deleted"})

    else:
        return respond(400, {"message": "Invalid request"})


def respond(status, body):
    return {
        "statusCode": status,
        "body": json.dumps(body)
    }

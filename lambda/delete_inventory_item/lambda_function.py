import boto3
import json
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    """
    Delete Inventory Item - DELETE
    """
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table('Inventory')

    item_id = event['pathParameters']['id']

    try:
        response = table.query(
            KeyConditionExpression=Key('item_id').eq(item_id)
        )

        items = response.get('Items', [])
        if not items:
            return {
                'statusCode': 404,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                    'Access-Control-Allow-Methods': 'GET,OPTIONS,POST,DELETE'
                },
                'body': json.dumps("Item not found")
            }

        item = items[0]

        table.delete_item(
            Key={
                'item_id': item['item_id'],
                'item_location_id': item['item_location_id']
            }
        )

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'GET,OPTIONS,POST,DELETE'
            },
            'body': json.dumps("Item deleted")
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'GET,OPTIONS,POST,DELETE'
            },
            'body': json.dumps(str(e))
        }
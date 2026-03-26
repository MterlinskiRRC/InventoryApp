import boto3
import json
import uuid
from decimal import Decimal

def lambda_handler(event, context):
    """
    Add Inventory Item - POST
    """
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table('Inventory')

    try:
        # Handle body parsing - could be string or already parsed dict
        if 'body' in event:
            body = event['body']
            if isinstance(body, str):
                body = json.loads(body)
        else:
            body = event
        
        new_item = {
            'item_id': str(uuid.uuid4()),
            'item_location_id': Decimal(str(body['item_location_id'])),
            'item_name': body['item_name'],
            'item_description': body['item_description'],
            'item_qty_on_hand': Decimal(str(body['item_qty_on_hand'])),
            'item_price': Decimal(str(body['item_price']))
        }

        table.put_item(Item=new_item)

        clean_item = json.loads(json.dumps(new_item, default=str))

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'GET,OPTIONS,POST,DELETE'
            },
            'body': json.dumps(clean_item)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'GET,OPTIONS,POST,DELETE'
            },
            'body': json.dumps({'error': str(e), 'type': type(e).__name__})
        }
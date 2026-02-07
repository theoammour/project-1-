import json
import boto3
import os
import uuid
from datetime import datetime

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))
    
    http_method = event.get('httpMethod')
    
    if http_method == 'GET':
        return get_all_items()
    elif http_method == 'POST':
        return create_item(event)
    else:
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Method not allowed'})
        }

def get_all_items():
    try:
        response = table.scan()
        items = response.get('Items', [])
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(items)
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def create_item(event):
    try:
        body = json.loads(event.get('body', '{}'))
        if not body or 'task' not in body:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing "task" field in body'})
            }
            
        item = {
            'id': str(uuid.uuid4()),
            'task': body['task'],
            'created_at': datetime.now().isoformat(),
            'status': 'pending'
        }
        
        table.put_item(Item=item)
        
        return {
            'statusCode': 201,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(item)
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

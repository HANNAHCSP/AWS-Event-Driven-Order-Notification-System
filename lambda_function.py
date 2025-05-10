import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
orders_table = dynamodb.Table('orders')

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, default=str))
    
    for record in event['Records']:
        try:
            message_body = record['body']
            try:
                order_data = json.loads(message_body)
                if isinstance(order_data, dict) and 'Message' in order_data:
                    order_data = json.loads(order_data['Message'])
            except json.JSONDecodeError:
                print("Message is not valid JSON, using as-is")
                order_data = {
                    'orderId': "ERROR-" + datetime.utcnow().isoformat(),
                    'error': 'Invalid JSON format',
                    'rawMessage': message_body
                }
            
            print("Processing order: " + json.dumps(order_data, default=str))
            validate_order_data(order_data)
            response = store_order(order_data)
            print("Successfully processed order: " + order_data.get('orderId', 'UNKNOWN'))
            print("DynamoDB response: " + json.dumps(response, default=str))
            
        except Exception as e:
            print("Error processing message: " + str(e))
            import traceback
            print(traceback.format_exc())
    
    return {
        'statusCode': 200,
        'body': json.dumps('Order processing complete')
    }

def validate_order_data(order_data):
    required_fields = ['orderId']
    for field in required_fields:
        if field not in order_data:
            raise ValueError("Required field '{}' missing in order data".format(field))

def store_order(order_data):
    if 'timestamp' not in order_data:
        order_data['timestamp'] = datetime.utcnow().isoformat()
    response = orders_table.put_item(Item=order_data)
    return response

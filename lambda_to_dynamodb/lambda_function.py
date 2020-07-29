import os
import json
import boto3
from urllib import parse

# Get the service resource.
dynamodb = boto3.resource('dynamodb')
# Instantiate a table resource object without actually
# creating a DynamoDB table. Note that the attributes of this table
# are lazy-loaded: a request is not made nor are the attribute
# values populated until the attributes
# on the table resource are accessed or its load() method is called.
table = dynamodb.Table('data')

data = {'statusCode': '200',
		'headers': {'Content-Type': 'application/json'}}

def put(identifier, timestamp, data):
	table.put_item(
		Item = {
			'identifier': identifier,
			'timestamp': timestamp,
			'data': data
		}
	)

def lambda_handler(event, context):
	res = parse.parse_qs(event['body'])
	put(res['identifier'][0], int(res['timestamp'][0]), res['data'][0])
	data['body'] = json.dumps({'result': 'success'})
	return data

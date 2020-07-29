import os
import json
import requests
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection

index = "mat"
doc_type = "nonono"

awsauth = AWS4Auth(
	os.environ['AWS_ACCESS_KEY_ID'],
	os.environ['AWS_SECRET_ACCESS_KEY'],
	os.environ['AWS_REGION'],
	'es',
	session_token=os.environ['AWS_SESSION_TOKEN']
)
es = Elasticsearch(
	hosts=[{'host': os.environ['ES_HOST'], 'port': 443}],
	http_auth=awsauth,
	use_ssl=True,
	verify_certs=True,
	connection_class=RequestsHttpConnection
)

def lambda_handler(event, context):
	dynamo = event['Records'][0]['dynamodb']['NewImage']
	data = {'identifier': dynamo['identifier']['S'],
			'timestamp': int(dynamo['timestamp']['N']),
			'data': dynamo['data']['S']}

	# curl -X POST 'https://#{ES_HOST}/#{index}/#{doc_type}' -d #{data}
	es.index(index=index, doc_type=doc_type, body=data)

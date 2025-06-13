import json
import boto3

boto3.setup_default_session(region_name='us-east-1')
ssm = boto3.client("ssm")
sns = boto3.client('sns')
SNS_TOPIC_ARN = ssm.get_parameter(Name="sns_topic")["Parameter"]["Value"]
DNS_NAME = ssm.get_parameter(Name="dns_name")["Parameter"]["Value"]


def lambda_handler(event, context):
    for record in event['Records']:
        body = json.loads(record['body'])
        message = (
            f"New image uploaded!\n"
            f"Name: {body['name']}\n"
            f"Size: {body['size']} bytes\n"
            f"Extension: {body['extension']}\n"
            f"Download: {DNS_NAME}/download/{body['name']}"
        )
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            MessageAttributes={
                'extension': {
                    'DataType': 'String',
                    'StringValue': body['extension']
                }
            }
        )
    return {"status": "ok"}
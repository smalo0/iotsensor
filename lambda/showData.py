import json
import boto3

def lambda_handler(event, context):
    # print statements available for troubleshooting
    if 'sensor_id' in event:
        sensor_id = event['sensor_id']
        print(sensor_id)

    function_name = context.function_name
    print(function_name)

    try:
        # Retrieve AWS credentials and region from environment variables
        aws_access_key_id = os.environ.get('AWS_AMPLIFY_ACCESS_KEY_ID')
        aws_secret_access_key = os.environ.get('AWS_AMPLIFY_SECRET_ACCESS_KEY')
        region = os.environ.get('AWS_DEFAULT_REGION')
        
        # Retrieve data from S3
        bucket_name = 'iot-sensordata-bucket'
        object_key = 'motion_sensor_data.json'
        s3_client = boto3.client("s3", region_name=region, aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key)
        
        # Your existing code to fetch data from S3
        key = 'motion_sensor_data.json'
        response = s3.get_object(Bucket=bucket_name, Key=key)
        data = response['Body'].read().decode('utf-8')
        json_data = json.loads(data)
        
        # Your existing code to process data
        print('Data:', json_data)
        
        return {
            'statusCode': 200,
            'body': json.dumps(json_data)
        }
    except Exception as e:
        print('Error:', e)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal Server Error'})
        }

event1 = {
    'time': '2024-04-21T12:00:00Z',
    'motion': 'detected',
    'sensor_id': '77475e31-3c2f-4a57-8a3a-2f06883deed8'
}


class DummyContext:
    def __init__(self):
        self.function_name = 'gcp_aws_data_upload'
        self.function_version = '1.0'
        # self.aws_request_id = '1234567890'


context1 = DummyContext()

lambda_result = lambda_handler(event1, context1)
print(lambda_result)


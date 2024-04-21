import json
import boto3 

def lambda_handler(event, context):
  file_path = "/tmp/motion_sensor_data.json"
  
  # Retrieve AWS credentials and region from environment variables
  aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
  aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
  region = os.environ.get('AWS_DEFAULT_REGION')
  
  # Store the results in S3
  bucket_name = 'iot-sensordata-bucket'
  object_key = 'motion_sensor_data.json'
  s3_client = boto3.client("s3", region_name=region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
  s3_client.upload_file(json_data, bucket_name, object_key)

  return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Data uploaded successfully'})
    }

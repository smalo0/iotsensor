import json
import boto3
from cassandra.cluster import Cluster

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Connect to Cassandra
    cluster = Cluster(['34.95.4.234'], port=9042)
    session = cluster.connect("motion")
    
    # Prepare and execute the query
    preparedStatement = session.prepare("SELECT * FROM motion_sensor_nosec WHERE state='True' ALLOW FILTERING;")
    rows = session.execute(preparedStatement)
    
    # Process the results
    result = []
    for row in rows:
        result.append(dict(row))
    
    # Close the Cassandra session and cluster
    session.shutdown()
    cluster.shutdown()

    json_data = json.dumps(result)
    file_path = "/tmp/motion_sensor_data.json"
    with open(file_path, "w") as file:
        file.write(json_data)
    
    # Retrieve AWS credentials and region from environment variables
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    region = os.environ.get('AWS_REGION')
    # Store the results in S3
    bucket_name = 'iot-sensordata-bucket'
    object_key = 'motion_sensor_data.json'
    s3_client = boto3.client("s3", region_name=region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    s3_client.upload_file(file_path, bucket_name, object_key)
    # s3.put_object(
        # Bucket=bucket_name,
        # Key=object_key,
        # Body=json_data
    # )
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Data retrieved successfully'})
    }

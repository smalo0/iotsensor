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
    
    # Store the results in S3
    bucket_name = 'iot-sensordata-bucket'
    object_key = 'motion_sensor_data.json'
    s3.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=json.dumps(result)
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Data stored in S3 successfully'})
    }

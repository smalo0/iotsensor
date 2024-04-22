import json
from cassandra.cluster import Cluster
import uuid
from datetime import datetime


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, uuid.UUID):
            return str(obj)
        return super().default(obj)


def lambda_handler(event, context):
    # print statements available for troubleshooting
    if 'sensor_id' in event:
        sensor_id = event['sensor_id']
        print(sensor_id)

    function_name = context.function_name
    print(function_name)

    # Connect to Cassandra
    cluster = Cluster(['34.95.4.234'], port=9042)
    session = cluster.connect("motion")

    # Prepare and execute the query
    prepared_statement = session.prepare("SELECT * FROM motion_sensor_nosec WHERE state='True' ALLOW FILTERING;")
    rows = session.execute(prepared_statement)

    # Convert from tuple to dictionary  
    database_rows = []
    for row_tuple in rows:
        row_dict = {
            'device_id': row_tuple[0],
            'timestamp': row_tuple[1],
            'state': row_tuple[2],
            'value': row_tuple[3]
        }
        database_rows.append(row_dict)
    
    # Process the results
    result = []
    for row in database_rows:
        row['device_id'] = str(row['device_id'])
        row['timestmap'] = row['timestamp'].isoformat()
        result.append(row)

    # Close the Cassandra session and cluster
    session.shutdown()
    cluster.shutdown()

    json_data = json.dumps(result, cls=CustomJSONEncoder)
    file_path = "/tmp/motion_sensor_data.json"
    with open(file_path, "w") as file:
        file.write(json_data)

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Data retrieved successfully'})
    }


event1 = {
    'time': '2024-04-21T12:00:00Z',
    'motion': 'detected',
    'sensor_id': '77475e31-3c2f-4a57-8a3a-2f06883deed8'
}


class DummyContext:
    def __init__(self):
        self.function_name = 'gcp_aws_data_connector'
        self.function_version = '1.0'
        # self.aws_request_id = '1234567890'


context1 = DummyContext()

lambda_result = lambda_handler(event1, context1)
print(lambda_result)


import json
from cassandra.cluster import Cluster


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

    # Process the results
    result = []
    for row in rows:
        result.append(dict(row))
        print(row)

    # Close the Cassandra session and cluster
    session.shutdown()
    cluster.shutdown()

    json_data = json.dumps(result)
    file_path = "/data/motion_sensor_data.json"
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


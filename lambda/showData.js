const AWS = require('aws-sdk');
const s3 = new AWS.S3();

exports.handler = async (event) => {
    try {
        const params = {
            Bucket: 'iot-sensordata-bucket',
            Key: 'motion_sensor_data.json'
        };
        const data = await s3.getObject(params).promise();
        const jsonData = JSON.parse(data.Body.toString('utf-8'));
        
        return {
            statusCode: 200,
            body: JSON.stringify(jsonData)
        };
    } catch (err) {
        return {
            statusCode: 500,
            body: JSON.stringify(err)
        };
    }
};

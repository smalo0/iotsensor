# iotsensor
Objective: user views motion sensor alert data on web page dashboard. Similar to a smart IoT home intrusion detection system. 
<!-- Insert Image of Dashboard -->

## lambda_function.py and upload_to_bucket.py: 
Initial database processing functions.
**lambda_function** retrieves data from GCP database with IAM authorization. Data serialization done for formatting.
  
![serialization-deserialization-diagram-800x318-1](https://github.com/smalo0/iotsensor/assets/128261499/1fb9b884-4f2f-4a6e-897e-537b7f50ecbb)
(hazelcast.com)
Output stored in temporary .json file.
**upload_to_bucket.py** moves the .json file to an AWS S3 bucket to be later used in web page. Credentials done with AWS Secrets Manager.
> [!NOTE]
> These functions only need to be run once. In a time-series implementation they would be synchronous with alerts.  

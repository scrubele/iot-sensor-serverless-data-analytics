import time
from google.cloud import pubsub_v1

project_id = "iot-data-processing-258913"
topic_name = "sensors" 

def publish_message(data):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    data = data.encode('utf-8')
    future = publisher.publish(
        topic_path, data, origin='python-sample', username='gcp'
    )
    print(future.result())

import time

from confluent_kafka import Producer, Consumer, KafkaError
import json

# USE kafka:9092 IN DEBUG maybe


producer = Producer({
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'my_producer_django'
})


consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my_consumer_django',
    'max.poll.interval.ms': 45000,
    # 'auto.offset.reset': 'latest'
})


consumer.subscribe(['response_topic'])


# Define callback function
def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')


# Send message
msg = {
    'time_django': time.time()
}
producer.produce('request_topic', value=json.dumps(msg).encode('utf-8'), callback=delivery_report)
producer.flush()

while True:
    msg = consumer.poll(timeout=1.0)
    if msg is None:
        continue

    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            print('End of partition event')
        else:
            print('Error while receiving message: {}'.format(msg.error()))
    else:
        response = json.loads(msg.value().decode("utf-8"))
        response['time_django2'] = time.time()
        response['delta_flask_to_django'] = response['time_django2'] - response['time_flask']

        print(response)
        break
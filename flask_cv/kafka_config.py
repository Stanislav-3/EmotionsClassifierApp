from confluent_kafka import Consumer, Producer, KafkaError
import json, time


producer = Producer({
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'my_producer_cv'
})

consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my_consumer_cv',
    'max.poll.interval.ms': 45000,
    # 'auto.offset.reset': 'latest'
})
consumer.subscribe(['request_topic'])


def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')


# Consume messages
while True:
    pass
    msg = consumer.poll(timeout=1.0)

    if msg is None:
        continue

    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            print(f'Reached end of partition {msg.partition()}')
        else:
            print(f'Error while consuming message: {msg.error()}')
    else:
        request = json.loads(msg.value().decode("utf-8"))

        request['time_flask'] = time.time()
        request['delta_django_to_flask'] = request['time_flask'] - request['time_django']
        print('Get data in flask', request)

        producer.produce('response_topic', value=json.dumps(request).encode('utf-8'), callback=delivery_report)
        producer.flush()

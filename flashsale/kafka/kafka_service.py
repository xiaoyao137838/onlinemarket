from kafka.producer import KafkaProducer
from kafka.consumer import KafkaConsumer
from decouple import config
import json

producer = KafkaProducer(bootstrap_servers=config('KAFKA_SERVER'))
print('Message queue is started', producer)

def key_deserializer(key):
    return key.decode('utf-8')

def value_deserializer(value):
    return json.loads(value.decode('utf-8'))

consumer_1 = KafkaConsumer(bootstrap_servers=config('KAFKA_SERVER'),
                          group_id=config('CREATE_ORDER_GROUP'),
                          key_deserializer=key_deserializer,
                          value_deserializer=value_deserializer,
                          enable_auto_commit=False,
                          api_version=(2, 5, 0))
consumer_1.subscribe([config('CREATE_ORDER_TOPIC')])


consumer_2 = KafkaConsumer(bootstrap_servers=config('KAFKA_SERVER'),
                          group_id=config('CHECK_PAY_STATUS_GROUP'),
                          key_deserializer=key_deserializer,
                          value_deserializer=value_deserializer,
                          enable_auto_commit=False,
                          api_version=(2, 5, 0))
consumer_2.subscribe([config('CHECK_PAY_STATUS_TOPIC')])

consumer_3 = KafkaConsumer(bootstrap_servers=config('KAFKA_SERVER'),
                          group_id=config('PAY_DONE_GROUP'),
                          key_deserializer=key_deserializer,
                          value_deserializer=value_deserializer,
                          enable_auto_commit=False,
                          api_version=(2, 5, 0))
consumer_3.subscribe([config('PAY_DONE_TOPIC')])

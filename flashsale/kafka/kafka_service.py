from kafka.producer import KafkaProducer
from kafka.consumer import KafkaConsumer
import json

producer = KafkaProducer(bootstrap_servers='192.168.99.100:9092')
print('Message queue is started', producer)

def key_deserializer(key):
    return key.decode('utf-8')

def value_deserializer(value):
    return json.loads(value.decode('utf-8'))

consumer_1 = KafkaConsumer(bootstrap_servers='192.168.99.100:9092',
                          group_id='CONSUMER_GROUP_1',
                          key_deserializer=key_deserializer,
                          value_deserializer=value_deserializer,
                          enable_auto_commit=False,
                          api_version=(2, 5, 0))
consumer_1.subscribe(['create_order'])


consumer_2 = KafkaConsumer(bootstrap_servers='192.168.99.100:9092',
                          group_id='CONSUMER_GROUP_2',
                          key_deserializer=key_deserializer,
                          value_deserializer=value_deserializer,
                          enable_auto_commit=False,
                          api_version=(2, 5, 0))
consumer_2.subscribe(['check_pay_status'])

consumer_3 = KafkaConsumer(bootstrap_servers='192.168.99.100:9092',
                          group_id='CONSUMER_GROUP_3',
                          key_deserializer=key_deserializer,
                          value_deserializer=value_deserializer,
                          enable_auto_commit=False,
                          api_version=(2, 5, 0))
consumer_3.subscribe(['pay_done'])

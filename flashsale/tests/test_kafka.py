from flashsale.kafka.kafka_service import key_deserializer, value_deserializer

def test_key_deserializer():
    key = key_deserializer(b'hello')
    assert key == 'hello'

def test_value_deserializer():
    value = value_deserializer(b'{"hello": 1}')
    assert value['hello'] == 1


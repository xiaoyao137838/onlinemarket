import redis
import json 
from vendor.models import OpeningHour
from django.forms.models import model_to_dict

redis_cli = redis.Redis('192.168.99.100')
print('Redis is started')

def create_flashsale(request, flashsale):
    add_vendor(request, flashsale)
    add_opening_hours(request, flashsale)
    add_product(request, flashsale)
    add_sale(request, flashsale)
    add_stock(request, flashsale)

def add_vendor(request, flashsale):
    key = f'flash.vendor:{flashsale.id}'
    vendor = request.user.id
    redis_cli.set(key, vendor)

def add_opening_hours(request, flashsale):
    vendor = request.user
    key = f'flash.opening-hour:{flashsale.id}'
    opening_hours = OpeningHour.objects.filter(vendor=vendor.id)
    value = json.dumps(list(opening_hours))
    redis_cli.set(key, value)

def add_product(request, flashsale):
    key = f'flash.product:{flashsale.id}'
    product = flashsale.product
    value = product.id
    redis_cli.set(key, value)

def add_sale(request, flashsale):
    key = f'flash.sale:{flashsale.id}'
    value = flashsale.id
    redis_cli.set(key, value)

def add_stock(request, flashsale):
    key = f'flash.stock:{flashsale.id}'
    available_count = flashsale.available_qty
    redis_cli.set(key, available_count)


def is_customer_qualified(request, flashsale_id):
    user_id = request.user.id
    key = f'flash-user:{flashsale_id}'
    if redis_cli.sismember(key, user_id):
        return False
    return True
    
def add_customer_to_limit(customer_id, flashsale_id):
    user_id = customer_id
    key = f'flash-user:{flashsale_id}'
    redis_cli.sadd(key, user_id)
    return True

def remove_customer_to_limit(customer_id, flashsale_id):
    user_id = customer_id
    key = f'flash-user:{flashsale_id}'
    redis_cli.srem(key, user_id)
    return True

def lock_stock(flashsale_id):
    key = f'flash.stock:{flashsale_id}'
    if not redis_cli.exists(key):
        return False
    
    pipe = redis_cli.pipeline()
    while True:
        try:
            pipe.watch(key)
            count = pipe.get(key)
            print('pipe created', count)

            if count <= b"0":
                pipe.unwatch()
                return False
            else:
                pipe.multi()
                pipe.decr(key)
                pipe.execute()
                return True
        except redis.WatchError:
            print('retrying...')
    
def reverse_stock(flashsale_id):
    key = f'flash.stock:{flashsale_id}'
    redis_cli.incr(key)
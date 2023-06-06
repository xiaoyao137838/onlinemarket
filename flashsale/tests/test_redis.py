
from django.test import RequestFactory

from flashsale.redis_service import is_customer_qualified, add_customer_to_limit, lock_stock, remove_customer_to_limit, reverse_stock


def test_is_customer_qualified(user, redis_cli, flash_sale_redis):
    request = RequestFactory()
    request.user = user
    print(user.id, flash_sale_redis.id)

    key = f'flash-user:{flash_sale_redis.id}' 
    redis_cli.srem(key, user.id)
    res = is_customer_qualified(request, flash_sale_redis.id)
    assert res == True
    
    redis_cli.sadd(key, user.id)
    res = is_customer_qualified(request, flash_sale_redis.id)
    assert res == False
    redis_cli.srem(key, user.id)

def test_add_customer_to_limit(user, redis_cli, flash_sale_redis):
    key = f'flash-user:{flash_sale_redis.id}' 
    assert False == redis_cli.sismember(key, user.id)
    add_customer_to_limit(user.id, flash_sale_redis.id)
    assert True == redis_cli.sismember(key, user.id)
    redis_cli.srem(key, user.id)

def test_remove_customer_to_limit(user, redis_cli, flash_sale_redis):
    key = f'flash-user:{flash_sale_redis.id}' 
    redis_cli.sadd(key, user.id)
    assert True == redis_cli.sismember(key, user.id)
    remove_customer_to_limit(user.id, flash_sale_redis.id)
    assert False == redis_cli.sismember(key, user.id)
    redis_cli.srem(key, user.id)

def test_lock_stock(redis_cli, flash_sale_redis):
    assert False == lock_stock('flash.stock:')

    key = f'flash.stock:{flash_sale_redis.id}' 
    pre_count = flash_sale_redis.total_qty
    redis_cli.set(key, flash_sale_redis.total_qty)
    lock_stock(flash_sale_redis.id)
    cur_count = redis_cli.get(key)
    assert pre_count - 1 == int(cur_count)
    redis_cli.set(key, pre_count)

def test_reverse_stock(redis_cli, flash_sale_redis):
    key = f'flash.stock:{flash_sale_redis.id}' 
    pre_count = flash_sale_redis.total_qty
    redis_cli.set(key, flash_sale_redis.total_qty)
    redis_cli.decr(key)
    cur_count = redis_cli.get(key)
    assert pre_count - 1 == int(cur_count)
    reverse_stock(flash_sale_redis.id)
    final_count = redis_cli.get(key)
    assert pre_count == int(final_count)
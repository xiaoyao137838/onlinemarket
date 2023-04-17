from order.request_object import RequestObjectMiddleware
def test_request_object():
    RequestObjectMiddleware(lambda x: x - 1)
    
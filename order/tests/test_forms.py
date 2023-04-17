from order.forms import OrderForm

def test_order_from_valid_data():
    form = OrderForm({})
    assert form.is_valid()
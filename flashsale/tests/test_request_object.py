from django.test import RequestFactory

from flashsale.context_processors import flash_sale_order

def test_flash_sale_order(customer, flash_sale):
    request = RequestFactory()
    request.user = customer

    res = flash_sale_order(request, flash_sale_id = flash_sale.id)
    assert isinstance(res, dict)

from market.models import CartItem, Tax

def test_cart_item_unicode(cart_item):
    unicode = cart_item.__unicode__()
    assert unicode == cart_item.product

def test_tax(tax):
    assert str(tax) == tax.tax_type
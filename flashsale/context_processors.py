from .models import FlashOrder

def flash_sale_order(request, flash_sale_id = None):
    try:
        flash_sale_order = FlashOrder.objects.get(customer=request.user, flash_sale=flash_sale_id)
    except:
        flash_sale_order = None
    
    return {
        'flash_sale_order': flash_sale_order
    }

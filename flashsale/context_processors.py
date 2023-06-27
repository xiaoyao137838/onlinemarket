from .models import FlashOrder
import logging

logger = logging.getLogger(__name__)

def flash_sale_order(request, flash_sale_id = None):
    try:
        flash_sale_order = FlashOrder.objects.get(customer=request.user, flash_sale=flash_sale_id, status__in=[0,1])
    except Exception as e:
        logger.error(e)
        flash_sale_order = None
    
    return {
        'flash_sale_order': flash_sale_order
    }

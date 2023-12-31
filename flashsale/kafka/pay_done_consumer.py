import os
import sys
import django
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.level = logging.DEBUG

module_path = os.getcwd()

path_folder = os.path.join(os.getcwd(), 'flashsale')

if path_folder in sys.path:
    sys.path.remove(path_folder)

if module_path not in sys.path:
    sys.path.append(module_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlinemarket.settings')
django.setup()

from flashsale.kafka.kafka_service import consumer_3
from flashsale.models import FlashOrder

logger.info('Pay-done consumer starts')
if __name__ == '__main__':
    for message in consumer_3:
        sale_order_no = message.value['sale_order_no']
        try:
            flash_order = FlashOrder.objects.get(order_no=sale_order_no, status=1)
            
            flash_sale = flash_order.flash_sale
            if flash_sale:
                logger.info(flash_sale.locked_qty)
                flash_sale.locked_qty -= 1
                flash_sale.save()
                logger.info('After pay done, available quantity: %s', flash_sale.available_qty)
                logger.info('After pay done, locked quantity: %s', flash_sale.locked_qty)
                
            logger.info('pay_done is consumed by message queue')
        except Exception as e:
            logger.info('No such flash sale or order found')
            logger.error(e)
       

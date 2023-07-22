import os
import sys
import django

module_path = os.getcwd()
path_folder = os.path.join(os.getcwd(), 'flashsale')

if path_folder in sys.path:
    sys.path.remove(path_folder)

if module_path not in sys.path:
    sys.path.append(module_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlinemarket.settings')
django.setup()

from flashsale.kafka.kafka_service import consumer_1
from flashsale.models import FlashSale, FlashOrder
from market.models import Tax
from accounts.models import User
from flashsale.utils import generate_order_no
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

logger.info('customer for loop 1')
if __name__ == '__main__':
    for message in consumer_1:
        data = message.value
        flash_sale_id = data['flash_sale_id']
        customer_id = data['customer_id']
    
        try:
            FlashOrder.objects.get(flash_sale=flash_sale_id, customer=customer_id, status__in=[0,1])
            logger.warning('This order is created or paied')
        except:
            try:
                flash_sale = FlashSale.objects.get(id=flash_sale_id)
                logger.info('Flash sale found: %s', flash_sale)
                product = flash_sale.product
                sub_amount = flash_sale.new_price
                tax_obj = Tax.objects.get(tax_type='Tax')
                tax_amount = sub_amount * float(tax_obj.percentage) / 100
                tax_data = {tax_obj.tax_type: { str(tax_obj.percentage): tax_amount }}
                total_amount = sub_amount + tax_amount
                logger.info('Before creating order, locked quantity: %s', flash_sale.locked_qty)
                logger.info('Before creating order, available quantity: %s', flash_sale.available_qty)

                if flash_sale.available_qty <= 0:
                    status = -1
                else:
                    flash_sale.available_qty -= 1
                    flash_sale.locked_qty += 1
                    flash_sale.save()
                    status = 0

                flash_order = FlashOrder.objects.create(
                    status=status,
                    customer=User(id=customer_id),
                    flash_sale=flash_sale,
                    product=product,
                    sub_amount=round(sub_amount, 2),
                    tax_amount=round(tax_amount, 2),
                    total_amount=round(total_amount, 2),
                    tax_data=json.dumps(tax_data)
                )
                flash_order.order_no = generate_order_no(flash_order)
                flash_order.save()
                logger.info('After creating order, locked quantity: %s', flash_sale.locked_qty)
                logger.info('After creating order, available quantity: %s', flash_sale.available_qty)
                logger.info('create_order is consumed by message queue')    
    
            except Exception as e:
                logger.error('This flashsale does not exist')
                logger.error(e)
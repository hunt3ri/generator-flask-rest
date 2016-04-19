from app.models.customers import Customer
from schematics import Model
from schematics.types import StringType, EmailType, DateTimeType, DecimalType
from schematics.types.compound import ListType, ModelType


class OrderItem(Model):
    """
    Describes an order item that a customer wishes to purchase
    """
    description = StringType(required=True)
    price = DecimalType(required=True)


class Order(Model):
    """
    Describes an order containing one or more OrderItems
    """
    order_id = StringType(serialized_name='orderId')
    order_status = StringType(serialized_name='orderStatus')
    customer_email_address = EmailType(serialized_name='customerEmailAddress')
    order_date = DateTimeType(serialized_name='orderDate')
    order_items = ListType(ModelType(OrderItem), min_size=1, serialized_name='orderItems')
    total_price_before_vat = DecimalType(required=True, serialized_name='totalPriceBeforeVat')
    total_vat = DecimalType(required=True, serialized_name='totalVat')
    total_price = DecimalType(required=True, serialized_name='totalPrice')


class CustomerOrder(Model):
    """
    Describes a distinct order made by a customer
    """
    customer = ModelType(Customer, required=True)
    order = ModelType(Order, required=True)

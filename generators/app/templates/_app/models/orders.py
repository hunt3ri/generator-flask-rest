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
    order_id = StringType()
    order_status = StringType()
    customer_email_address = EmailType()
    order_date = DateTimeType()
    order_items = ListType(ModelType(OrderItem), min_size=1)
    price_before_vat = DecimalType(required=True)
    total_vat = DecimalType(required=True)
    total_price = DecimalType(required=True)


class CustomerOrder(Model):
    """
    Describes a distinct order made by a customer
    """
    customer = ModelType(Customer, required=True)
    order = ModelType(Order, required=True)

from enum import Enum
import os
import uuid
from datetime import datetime
from app.stores.dynamo.utils import initialise_dynamo_connection
from app.models.orders import Order


class OrderStatus(Enum):
    """
    Enum to describes all possible states of an Order
    """
    IN_PROGRESS = 1
    SUCCESS = 2
    FAILED = 3


class OrderStoreError(Exception):
    """
    Custom exception to notify the caller an order has failed to save in Dynamo DB.
    """
    pass


class OrdersStore:

    dynamodb = None
    orders_table = None

    def _get_table_name(self):
        """
        Get the table name for the current environment
        """
        env = os.getenv('FLASK_MICRO_CONFIG', 'Dev')
        return str('flask_micro.{}.orders').format(env).lower()

    def __init__(self, config=None):
        """
        Setup necessary objects for negotiating with dynamo
        :param config: Optional config param most useful for testing
        """
        if config is None:
            self.dynamodb = initialise_dynamo_connection()
        else:
            self.dynamodb = initialise_dynamo_connection(config)

        table_name = self._get_table_name()
        self.orders_table = self.dynamodb.Table(table_name)

    def save(self, order):
        """
        Save order to database, all orders must be associated with a customer
        :param order: The order to save
        :returns order: Returns the order, with order_id and other meta-data applied
        """

        order = Order(order)

        order_id = str(uuid.uuid4()).upper()[:8]
        order.order_id = order_id
        order.order_date = datetime.now()
        order.order_status = OrderStatus.SUCCESS.name

        try:
            self.orders_table.put_item(
                Item=order.to_primitive()
            )
        except TypeError as e:
            error_message = 'Error occurred attempting to Save order. Exception {0}, Order {1}'.format(str(e),
                                                                                                order.to_primitive())
            raise OrderStoreError(error_message)

        # Get the item which will demonstrate it was successfully created
        return self.get(order.customer_email_address, order.order_id)

    def get(self, customer_email_address, order_id):
        """
        Gets the order object for the supplied email and order_id
        :param customer_email_address: email_address being searched
        :param order_id: order_id required
        :raises ValueError if order not found
        :returns Order mathing search criteria
        """
        response = self.orders_table.get_item(
            Key={
                'customerEmailAddress': customer_email_address,
                'orderId': order_id
            }
        )

        try:
            item = response['Item']
        except KeyError:
            raise ValueError(str('No order found for email address: {0}, order_id {1}').format(customer_email_address,
                                                                                               order_id))

        order = Order(item)
        return order


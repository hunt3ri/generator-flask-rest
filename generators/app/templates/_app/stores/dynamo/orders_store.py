from enum import Enum
import decimal
import os
import uuid
from datetime import datetime
from boto3.dynamodb.conditions import Key
from app.stores.dynamo.utils import initialise_dynamo_connection
from app.models.customers import Customer
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

    def save(self, order, customer, order_status):
        """
        Save order to database, all orders must be associated with a customer
        :param order: The order to save
        :param customer: The customer who owns the order
        :param order_status: The state of the order when it's saved
        :returns order: Returns the order, with order_id and other meta-data applied
        """
        if type(order_status) is not OrderStatus:
            raise TypeError("order_status is invalid Type, must be of type OrderStatus")

        order = Order(order)
        customer = Customer(customer)

        # Associate order with customer who made it
        order.customer_email_address = customer.email_address

        # Generate order id, because orders are associated with email addresses we should be safe to truncate
        # uuid to 8 chars, as collisions are extremely unlikely
        order_id = str(uuid.uuid4()).upper()[:8]
        order.order_id = order_id

        order.order_date = datetime.now()
        order.order_status = order_status.name

        try:
            self.orders_table.put_item(
                Item=order.to_primitive()
            )
        except TypeError as e:
            error_message = 'Error occurred attempting to Save order. Exception {0}, Order {1}'.format(str(e),
                                                                                                order.to_primitive())
            raise OrderStoreError(error_message)

        # Get the item which will demonstrate it was successfully created
        return self.get(customer.email_address, order_id)

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

    def get_all(self, customer_email_address):
        """
        Return all orders that match the supplied email address
        :param customer_email_address: Customer Email Address
        :raises ValueError if no matching orders found
        :returns List of matching Orders
        """
        response = self.orders_table.query(
            KeyConditionExpression=Key('customerEmailAddress').eq(customer_email_address)
        )

        items = response['Items']
        orders = []

        # Iterate over matching order items and cast them to strongly typed Order models
        for order in items:
            orders.append(Order(order))

        return orders

    def update_order_status(self, order, order_status):
        """
        Updates the status of the order
        :param order:
        :param order_status:
        :return: The updated order model
        """
        if type(order_status) is not OrderStatus:
            raise TypeError("order_status is invalid Type, must be of type OrderStatus")

        # If order not found exception will propogate upwards which is what we want
        order = self.get(order.customer_email_address, order.order_id)
        order.order_status = order_status.name

        self.orders_table.update_item(
            Key={
                'customerEmailAddress': order.customer_email_address,
                'orderId': order.order_id
            },
            UpdateExpression='SET orderStatus = :orderStatus',
            ExpressionAttributeValues={
                ':orderStatus': order.order_status
            }
        )

        return order

    def _delete(self, customer_email_address, order_id):
        """
        Delete method only exists for testing, and it's extremely unlikely we'll want to delete orders once they
        are created
        """
        self.orders_table.delete_item(
            Key={
                'customerEmailAddress': customer_email_address,
                'orderId': order_id
            }
        )

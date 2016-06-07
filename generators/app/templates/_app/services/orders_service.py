from app.models.orders import Order
from app.stores.dynamo.orders_store import OrdersStore, OrderStoreError


class OrderError(Exception):
    """
    Custom exception to notify callers an error has occured
    """


class OrdersService:

    def create_order(self, order):
        """
        Create and store order
        :param order: The order in scope
        :raises:
        :return: The created order
        """

        try:
            order = Order(order)
            order_store = OrdersStore()
            saved_order = order_store.save(order)
            return saved_order
        except OrderStoreError:
            raise OrderError('Error occurred saving order')

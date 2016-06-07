from flask_restful import Resource, request
from app.models.orders import Order
from app.services.orders_service import OrdersService, OrderError
from schematics.exceptions import DataError
from app import app


class Orders(Resource):
    """
    /orders
    """

    def put(self):
        """
        Place an order and make a payment.
        ---
        tags:
          - orders
        consumes:
          - application/json
        parameters:
          - in: body
            name: body
            required: true
            description: Json object for an order
            schema:
              type: object
              properties:
                customerEmailAddress:
                  type: string
                  default: test@test.com
                orderItems:
                  type: array
                  items:
                    type: object
                    properties:
                      description:
                        type: string
                        default: Test Item
                      price:
                        type: float
                        default: 10.00
                totalPriceBeforeVat:
                  type: float
                  default: 10.00
                totalVat:
                  type: float
                  default: 2.10
                totalPrice:
                  type: float
                  default: 12.10
        """
        try:
            order = Order(request.get_json())
            order.validate()
        except DataError as e:
            return {'Error': str(e)}, 400

        # Process order
        try:
            order_service = OrdersService()
            order = order_service.create_order(order)
            return {'orderId': order.order_id, 'orderStatus': order.order_status}, 201
        except OrderError:
            return {'Order Failed Reason': 'Error saving order'}, 500
        except Exception as e:
            app.logger.error('Unhandled error: {0}'.format(str(e)))
            return {'Order Failed Reason': 'Unhandled exception'}, 500

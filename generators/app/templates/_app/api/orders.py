from flask_restful import Resource


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
        pass

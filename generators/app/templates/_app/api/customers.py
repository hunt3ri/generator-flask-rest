from flask_restful import Resource, request
from app.models.customers import Customer
from schematics.exceptions import DataError
from app.services.customer_service import CustomerService, CustomerServiceError


class Customers(Resource):
    """
    /api/customers
    """

    def put(self):
        """
        Get a customer
        ---
        tags:
          - customers
        produces:
          - application/json
        parameters:
          - in: body
            name: body
            required: true
            description: Json request for creating account
            schema:
              type: object
              properties:
                firstName:
                  type: string
                  default: Test
                surname:
                  type: string
                  default: McTest
                emailAddress:
                  type: string
                  default: test.mctest@test.com
        responses:
          201:
            description: Customer Created
          400:
            description: Invalid Request
          500:
            description: Server Error
        """
        # Validate request, return 400 if invalid
        try:
            customer = Customer(request.get_json())
            customer.validate()
        except DataError as e:
            return {'Error': str(e)}, 400

        try:
            customer_service = CustomerService()
            customer_service.create_or_get_customer(customer)
            return {'Status': 'SUCCESS'}, 201
        except CustomerServiceError:
            return {'Status': 'ERROR'}, 500

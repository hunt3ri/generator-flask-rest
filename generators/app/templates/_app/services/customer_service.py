from app.models.customers import Customer
from app.stores.dynamo.customer_store import CustomerStore, CustomerStoreError
from app import app


class CustomerServiceError(Exception):
    """
    Custom exception to notify the caller error has occurred within the CustomerStore
    """
    pass


class CustomerService:

    def create_or_get_customer(self, customer):
        """
        Get customer if it exists in database, otherwise create.
        :param customer: Customer object we're looking for
        :returns customer: Customer
        """
        customer_store = CustomerStore()

        database_customer = customer_store.get(customer.email_address)

        if database_customer:
            return database_customer

        # Cust doesn't exist so save them
        try:
            customer_store.save(customer)
            return Customer(customer)
        except CustomerStoreError:
            app.logger.debug('Error creating customer {0}'.format(customer.email_address))
            raise CustomerServiceError("Error creating customer")

    def get_customer_by_email(self, email_address):
        """
        Gets customer by email address returns none if not found
        :param email_address: Email address in scope
        :return: Customer or None
        """
        customer_store = CustomerStore()

        customer = customer_store.get(email_address)

        return customer

import os
import app.stores.dynamo.utils as utils
from botocore.exceptions import ClientError
from app.models.customers import Customer
from app import app


class CustomerStoreError(Exception):
    """
    Custom exception to notify the caller error has occurred within the CustomerStore
    """
    pass


class CustomerStore:

    # Config is injectable for ease of testing
    config = None
    dynamodb = None
    customer_table = None

    def _get_table_name(self):
        """
        Get the table name for the current environment
        """
        env = os.getenv('FLASK_MICRO_CONFIG', 'Dev')
        return 'flask_micro.{}.customers'.format(env).lower()

    def __init__(self):
        """
        Setup necessary objects for negotiating with dynamo
        :param config: Optional config param most useful for testing
        """
        if self.config is None:

            self.dynamodb = utils.initialise_dynamo_connection()
        else:
            self.dynamodb = utils.initialise_dynamo_connection(self.config)

        table_name = self._get_table_name()
        self.customer_table = self.dynamodb.Table(table_name)

    def save(self, customer):
        """
        Save supplied customer object to database
        """
        try:
            cust = Customer(customer)
            self.customer_table.put_item(
                Item=cust.to_primitive()
            )
        except ClientError as e:
            app.logger.error('Error saving customer record {0}, exception {1}'.format(customer.email_address, str(e)))
            raise CustomerStoreError('Error saving customer record {0}, exception {1}'.format(customer.email_address,
                                                                                              str(e)))

    def get(self, email_address):
        """
        Gets customer for supplied email address
        :param email_address: email address for the customer you are searching for
        :raises ValueError if customer not found
        :returns Customer matching the email address
        """
        response = self.customer_table.get_item(
            Key={
                'emailAddress': email_address
            }
        )

        try:
            item = response['Item']
        except KeyError:
            # Return None if no customer found, it is NOT exceptional for customer not to exist
            return None

        customer = Customer(item)
        return customer

    def update(self, customer):
        """
        Updates the entire customer record
        """

        # Ensure customer exists prior to update, otherwise we'll create a new cust record which is likely to
        # confuse the caller
        self.get(customer.email_address)

        self.customer_table.update_item(
            Key={
                'emailAddress': customer.email_address
            },
            UpdateExpression='SET firstName = :firstName, surname = :surname',
            ExpressionAttributeValues={
                ':firstName': customer.first_name,
                ':surname': customer.surname
            }
        )

    def delete(self, email_address):
        """
        Deletes customer for supplied email address
        :param email_address: email address for the customer you want to delete
        """

        # Ensure cust exists prior to deletion
        self.get(email_address)

        self.customer_table.delete_item(
            Key={
                'emailAddress': email_address
            }
        )

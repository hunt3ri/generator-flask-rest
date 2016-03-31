from schematics import Model
from schematics.types import EmailType, StringType


class Customer(Model):
    """
    Model that describes a MapStore customer
    """
    first_name = StringType(required=True)
    surname = StringType(required=True)
    email_address = EmailType(required=True)

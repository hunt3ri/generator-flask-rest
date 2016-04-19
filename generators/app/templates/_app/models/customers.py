from schematics import Model
from schematics.types import EmailType, StringType


class Customer(Model):
    """
    Model that describes a basic customer
    """
    first_name = StringType(required=True, serialized_name='firstName')
    surname = StringType(required=True)
    email_address = EmailType(required=True, serialized_name='emailAddress')

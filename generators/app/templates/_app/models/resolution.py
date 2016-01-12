from mongoengine import *


class Resolution(Document):

    title = StringField(required=True)

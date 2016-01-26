from flask import abort
from mongoengine.queryset import MultipleObjectsReturned, DoesNotExist
from mongoengine.base import ValidationError, FieldDoesNotExist
from mongoengine import Document, StringField
from app.models.dto import DTOs
from app.stores.mongo.mongo_store import MongoStore

class Resolution(Document):
    """
    Mongo Document representation of Resolution
    """

    title = StringField(required=True)


class MongoResolutionStore(MongoStore):
    """
    Mongo implementation of ResolutionStore
    """

    def get_or_404(self, res_id):
        """
        Gets the object for the specified id, if not found aborts the proces and returns 404
        :param res_id: Id for the Resolution you're looking for
        :return: ResolutionDTO named tuple
        """

        try:
            resolution = Resolution.objects.get(id=res_id)
        except (MultipleObjectsReturned, DoesNotExist, ValidationError):
            abort(404)

        resolution_dict = self.get_dict(resolution, 'res_id')

        resolution_dto = DTOs.ResolutionDTO(**resolution_dict)

        return resolution_dto

    def save(self, resolution_json):
        """
        Takes the supplied Json and translates it to a mongo object, before saving to the database
        :param resolution_json: Resolution defined as Json
        :return: New resolution object
        """

        try:
            resolution = Resolution.from_json(resolution_json)
        except FieldDoesNotExist as e:
            abort(500, 'Field Does Not Exist Error: ' + str(e))

        resolution.save()

        resolution_dict = self.get_dict(resolution, 'res_id')

        resolution_dto = DTOs.ResolutionDTO(**resolution_dict)

        return resolution_dto

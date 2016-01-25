from flask import abort
from mongoengine.queryset import MultipleObjectsReturned, DoesNotExist
from mongoengine.base import ValidationError
from mongoengine import Document, StringField
from app.models.dto import DTOs

class Resolution(Document):
    """
    Mongo Document representation of Resolution
    """

    title = StringField(required=True)


class MongoResolutionStore:
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

        resolution_dict = resolution.to_mongo().to_dict()

        # TODO add helper or base class to make this generic
        temp_id = str(resolution_dict['_id'])
        resolution_dict.pop('_id')
        resolution_dict['id'] = temp_id

        resolution_dto = DTOs.ResolutionDTO(**resolution_dict)

        return resolution_dto

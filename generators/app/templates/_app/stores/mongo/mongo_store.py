class MongoStore:
    """
    Base class containing useful functions for Mongo Store classes
    """

    @staticmethod
    def get_dict(document, new_id_field_name):
        """
        Takes a Mongo document and translates it into a Python dictionary, replacing the unfriendly _id field with
        the field specified
        :param document: The Mongo Doc to translate id for
        :param new_id_field_name: The new id field name
        :return: Python Dict version of the document.
        """

        # Here we're translating the mongo BSON format to something more paletable for the python world
        friendly_dict = document.to_mongo().to_dict()

        # Replace mongo specific _id field with the DTO id field
        temp_id = str(friendly_dict['_id'])
        friendly_dict.pop('_id')
        friendly_dict[new_id_field_name] = temp_id

        return friendly_dict

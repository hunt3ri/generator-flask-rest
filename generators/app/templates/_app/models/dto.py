from collections import namedtuple


class DTOs:
    """
    Class is a holder for Data Transer Objects (DTOs) allowing us to make the code more expressive and readable
    rather than passing anonymous dictionaries or tuples back and forth
    """

    ResolutionDTO = namedtuple('ResolutionDTO', [
        'res_id',
        'title'])

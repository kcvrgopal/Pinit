

from couchdb.mapping import Document,TextField,IntegerField,ListField,DictField,Mapping

class User(Document):
    """
    This class contains fields for User related information
    """
    username=TextField()
    password=TextField()
    name=TextField()

class Pin(Document):
    """
    This class contains fields for Pin related information
    """
    user_id=TextField()
    pin_url=TextField()
    pin_name=TextField()
    comments=ListField(DictField(Mapping.build(user_id=TextField(),
                                               comment=TextField())))


class Board(Document):
    """
    This class contains fields for Board related information
    """
    user_id=TextField()
    board_name=TextField()
    board_type=TextField()
    pins=ListField(DictField(Mapping.build(pin_id=TextField())))

class Counttrack(Document):
    """
    This class contains fields for Count related information
    """
    entity=TextField()
    count=IntegerField()
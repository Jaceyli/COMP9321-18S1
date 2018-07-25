from mongoengine import StringField, IntField, Document, EmbeddedDocumentField, ListField, EmbeddedDocument


class Detail(EmbeddedDocument):
    id = IntField(required=True, primary_key=True)
    offence_group = StringField(required=True, max_length=100)
    offence_type = StringField(required=True, max_length=200)
    period = StringField(required=False, max_length= 20)
    record_type = StringField(required=True,max_length=50)
    value = StringField(required=False,max_length=1000000)

    def __init__(self, id, offence_group, offence_type,  period, record_type, value="",*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id
        self.offence_group = offence_group
        self.offence_type = offence_type
        self.period = period
        self.record_type = record_type
        self.value = value

class Record(Document):
     id = IntField(required=True, primary_key=True)
     title = StringField(required=True, max_length=200)
     description = StringField(required=True, max_length=400)
     area = StringField(required=True, max_length=50)
     details = ListField(EmbeddedDocumentField(Detail))

     def __init__(self, id, title, description, area, details=[], *args, **values):
        super().__init__(*args, **values)
        self.id = id
        self.title = title
        self.description = description
        self.area = area
        self.details = details

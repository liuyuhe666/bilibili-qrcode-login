from peewee import *

from modules.types import LoginRequestState

db = SqliteDatabase('database.db')


class BaseModel(Model):
    class Meta:
        database = db


class LoginRequest(BaseModel):
    id = PrimaryKeyField()
    uuid = CharField(255, unique=True)
    url = CharField(256)
    qrcode_key = CharField(256)
    state = IntegerField(default=LoginRequestState.Pending)
    created_at = BigIntegerField(default=0)

    class Meta:
        table_name = 'login'
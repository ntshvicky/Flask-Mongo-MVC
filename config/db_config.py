import mongoengine

from config.constants import DB_HOST, DB_NAME

alias = 'default'
data = dict(
    host=DB_HOST,
    port=27017,
    ssl=False)


def global_init():
    mongoengine.register_connection(alias=alias, name=DB_NAME, **data)
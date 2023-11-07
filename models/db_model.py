from datetime import datetime
import mongoengine as db

class User(db.Document):
    fullname = db.StringField(required=True)
    username = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    email = db.StringField(required=True)
    mobile = db.StringField()
    agree = db.IntField(required=True)
    login_token = db.StringField()
    login_token_date = db.DateTimeField()
    created = db.DateTimeField(required=True, default=datetime.utcnow)
    role = db.StringField(default="users") # users, admin

    meta = {
        'db_alias': 'default', #database alias name
        'collection': 'users' #table name in database
    }

class Employees(db.Document):
    user_id = db.ReferenceField('User')
    emp_code = db.StringField(required=True, unique=True)
    name = db.StringField(required=True)
    designation = db.StringField(required=True)
    profile = db.StringField()
    created = db.DateTimeField(required=True, default=datetime.utcnow) # set by default time

    meta = {
        'db_alias': 'default', #database alias name
        'collection': 'employees' #table name in database
    }


class Logs(db.Document):
    action = db.StringField()
    ip_address = db.StringField()
    req_header = db.StringField()
    browser = db.StringField() #chrome, firefox, safari, opera
    platform = db.StringField() #ios, android, windows, macos
    mobile = db.StringField()
    referer = db.StringField() #Referer
    city = db.StringField()
    country = db.StringField()
    region = db.StringField() 
    latitude = db.StringField() 
    longitude = db.StringField() 
    timezone = db.StringField() 
    log_date = db.DateTimeField(required=True, default=datetime.utcnow) # set by default time
    called_api = db.StringField() 
    user_id = db.StringField()
    emp_id = db.StringField()
    req_data = db.StringField()

    meta = {
        'db_alias': 'default', #database alias name
        'collection': 'logs' #table name in database
    }
    


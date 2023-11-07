
# Import necessary modules
from datetime import datetime, timedelta
from config.constants import APP_SECRET_KEY
from models.route_model import UpdateProfile, UserCreate, UserLogin
import bcrypt

from bson import ObjectId
from mongoengine.errors import NotUniqueError
import logging

import jwt

import os

from models.db_model import User


# eaxmple of register new user
def register(userData: UserCreate, role: str = "users"):
    try:
        obj = User()
        obj.fullname = userData.fullname.strip()
        obj.username = userData.username.strip()
        obj.email = userData.email.lower().strip()
        obj.mobile = userData.mobile.strip()
        obj.password = bcrypt.hashpw(userData.password.strip().encode('utf-8'), bcrypt.gensalt()).decode('utf-8') 
        obj.agree = 1
        obj.role = 'users'
        obj.save()
        return True, str(obj.id)
    except NotUniqueError as e:
        logging.error(f"Integrity Error: {e}")
        return False, 'Duplicate username'
    except Exception as e:
        logging.error(f"Exception: {e}")
        return False, 'Insertion failed'

# example of login user and create login token
def login(user: UserLogin):

    user_record = User.objects(username__iexact=user.username, agree=1).first()
    if user_record is not None and bcrypt.checkpw(user.password.encode('utf-8'), user_record.password.encode('utf-8')):
        user_record = user_record.to_mongo()
        del user_record['password']
        user_record['_id'] = str(user_record['_id'])

        # validate token for one day
        token = jwt.encode({'public_id' : str(user_record['_id']), 'exp' : datetime.utcnow() + timedelta(minutes=1440)}, APP_SECRET_KEY, algorithm="HS256")
        if token is not None:
            user_record['login_token'] = token.decode('utf-8')
            user_record['login_token_date'] = datetime.utcnow()
            res = update_token(user_record['_id'], user_record['login_token'], user_record['login_token_date'])
            if res > 0:
                return user_record
            
        return None
    else:
        return None
    
# example of read user data by user id
def getUser(user_id):
    try:

        user_record = User.objects(id=ObjectId(user_id), agree=1).first()
        if user_record is not None:
            user_record = user_record.to_mongo()
            del user_record['password']
            if 'login_token' in user_record:
                del user_record['login_token']
            if 'login_token_date' in user_record:
                del user_record['login_token_date']
            del user_record['_sa_instance_state']
        return user_record
    except Exception as e:
        logging.error(f"Exception: {e}")
        return None


# example of read user data by user id and role
def validate_user(id: str, role: str = "users"):
    try:
        user_record = User.objects(id=ObjectId(id), role__iexact=role, agree=1).first()
        # add required logic to validate user
        return user_record is not None
    except Exception as e:
        logging.error(f"Exception: {e}")
        return False

# function to validate user token
def validateUserToken(user_id: str, token: str):

    user_record = User.objects(id=ObjectId(user_id), agree=1).first()
    
    if user_record is None:
        return False
    
    if user_record.login_token != token:
        return False
    
    current_time = datetime.utcnow()
    time_difference = current_time - user_record.login_token_date

    if time_difference < timedelta(minutes=1440):
        return True
    
    return False

# function to update user login token
def update_token(user_id: str, token: str, login_token_date: datetime):
    try:
        user_record = User.objects(id=ObjectId(user_id), agree=1).first()
        if user_record:
            user_record.login_token=token
            user_record.login_token_date=login_token_date
            user_record.save()
            return True
    except Exception as e:
        logging.error(f"Exception: {e}")
        return False

# example of update user details
def update_details(userData: UpdateProfile):
    try:
        user_record = User.objects(id=ObjectId(userData.profile_id), agree=1)
        if user_record:
            user_record.fullname=userData.fullname, 
            user_record.mobile=userData.mobile, 
            user_record.agree=userData.status
            return True, 'User record updated'
    except Exception as e:
        logging.error(f"Exception: {e}")
        return False, 'User record update failed'

# example of list all users with pagination
def list_users(filterArr: any, offset: int = 0, limit: int = 10, orderset: str = "desc"):
    user_res = User.objects(__raw__= filterArr)
    total_count = user_res.count()
    user_res = user_res.order_by(orderset).skip(offset).limit(limit)
    dList = []
    if user_res is not None:
        for d in user_res:
            d = d.to_mongo()
            d['_id'] = str(d['_id'])
            del d['password']
            dList.append(d)
    return total_count, dList
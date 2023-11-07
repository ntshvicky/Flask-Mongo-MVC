
# Import necessary modules
from models.db_model import Employees
from models.route_model import EmpData, EmpUpdate

from bson import ObjectId
from mongoengine.errors import NotUniqueError

import logging

def create_employees(empData: EmpData):
    try:
        obj = Employees()
        obj.user_id=ObjectId(empData.user_id)
        obj.emp_code=empData.emp_code
        obj.name=empData.name
        obj.designation=empData.designation
        obj.save()
        return True, str(obj.id)
    except NotUniqueError as e:
        logging.error(f"Integrity Error: {e}")
        return False, 'Duplicate employee code'
    except Exception as e:
        logging.error(f"Exception: {e}")
        return False, f"Exception: {e}"

def get_employee_obj(pid: str):
    try:
        return Employees.objects(id=ObjectId(pid)).first()
    except Exception as ex:
        print(str(ex))
        return None
    
def update_profile_image(pid: str, profile: any):
    try:
        emp_record = get_employee_obj(pid)
        if emp_record:
            res = Employees.objects(id=ObjectId(pid)).update(set__profile=profile)
            if res > 0:
                return True
        return False
    except Exception as e:
        logging.error(f"Exception: {e}")
        return False

def update_employee_data(emp: EmpUpdate):
    try:
        emp_record = get_employee_obj(emp.emp_id)
        if emp_record:
            update_dict = {
                "set__name": emp.name,
                "set__designation": emp.designation
            }

            # you can add more fields here if you want to update the data using if else statements
            # example: 
            # if image_url is not None:
            #   update_dict['set__profile'] = profile
            update_query = {}
            for key, value in update_dict.items():
                update_query[key] = value
            
            res = Employees.objects(id=ObjectId(emp.emp_id)).update(**update_query)
            if res > 0:
                return True
        return False
    except Exception as e:
        logging.error(f"Exception: {e}")
        return False


def delete_employee(emp_id):
    try:

        res = Employees.objects(id=ObjectId(emp_id)).delete()
        if res > 0:
            return True
        return False
    except Exception as e:
        logging.error(f"Exception: {e}")
        return False

def count_employees():
    return Employees.objects().count()

def get_employee_by_code(emp_code: str):
    emp_record = Employees.objects(emp_code__iexact=emp_code).first()
    if not emp_record:
        return None
    
    emp_record = emp_record.to_mongo()
    emp_record['_id'] = str(emp_record['_id'])
    emp_record['user_id'] = str(emp_record['user_id'])
    return emp_record

def get_employee(emp_id):
    emp_record = get_employee_obj(emp_id)
    if not emp_record:
        return None
    
    emp_record = emp_record.to_mongo()
    emp_record['_id'] = str(emp_record['_id'])
    emp_record['user_id'] = str(emp_record['user_id'])
    return emp_record

def list_employees(filterArr: any, offset: int = 0, limit: int = 10, orderset: str = "desc"):

    emp_res = Employees.objects(__raw__= filterArr)
    total_count = emp_res.count()
    emp_res = emp_res.order_by(orderset).skip(offset).limit(limit)
    dList = []
    if emp_res is not None:
        for d in emp_res:
            d = d.to_mongo()
            d['_id'] = str(d['_id'])
            d['user_id'] = str(d['user_id'])
            dList.append(d)
    return total_count, dList


# Import necessary modules
import logging
from helpers.extra_helpers import getIPDetails
from bson import ObjectId

from models.db_model import Logs

# save log
def saveChangeLog(
        user_id: str,
        action: str,
        ip_address: str,
        request_header: dict,
        browser: str,
        platform: str,
        mobile: str,
        referer: str,
        called_api: str,
        emp_id: str,
        req_data: str
):
    try:
        gloc = getIPDetails(ip_address)
        obj = Logs()
        obj.user_id = user_id
        obj.action = action
        obj.ip_address = ip_address
        obj.req_header = request_header
        obj.browser = browser
        obj.platform = platform
        obj.referer = referer
        obj.mobile = mobile
        obj.city = None if 'geoplugin_city' not in gloc else gloc['geoplugin_city']
        obj.country = None if 'geoplugin_countryName' not in gloc else gloc['geoplugin_countryName']
        obj.region = None if 'geoplugin_continentName' not in gloc else gloc['geoplugin_continentName']
        obj.latitude = None if 'geoplugin_latitude' not in gloc else gloc['geoplugin_latitude']
        obj.longitude = None if 'geoplugin_longitude' not in gloc else gloc['geoplugin_longitude']
        obj.timezone = None if 'geoplugin_timezone' not in gloc else gloc['geoplugin_timezone']
        obj.called_api = called_api
        obj.emp_id = emp_id
        obj.req_data = req_data
        obj.save()
        return str(obj.id)
    except Exception as e:
        logging.error(f"Integrity Error: {e}")
        return None



# example of list all logs
def list_logs(filterArr: any, offset: int = 0, limit: int = 10, orderset: str = "desc"):
    log_res = Logs.objects(__raw__= filterArr)
    total_count = log_res.count()
    log_res = log_res.order_by(orderset).skip(offset).limit(limit)
    dList = []
    if log_res is not None:
        for d in log_res:
            d = d.to_mongo()
            d['_id'] = str(d['_id'])
            dList.append(d)
    return total_count, dList

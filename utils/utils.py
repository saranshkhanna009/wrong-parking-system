###########################
# Utilities Functions
###########################

# python imports
import requests
import datetime 

# django imports
from django.conf import settings

# inner app imports

def get_first_and_last_name(name):
    """
    Returns first and last name from a given name
    """
    name = name.strip()
    name_parts = name.split()
    if len(name_parts) > 1:
        first_name = name_parts[0]
        last_name = ' '.join(name_parts[1:])
        return first_name, last_name
    return name, ''


def check_float(potential_float):
    try:
        float(potential_float)
        return True
    except ValueError:
        return False   

def check_date(date_string):
    try:
        format = "%Y-%m-%d"
        datetime.datetime.strptime(date_string, format)
        return True
    except ValueError:
        return False


def send_sms_api(mobile, message,temp_id=''):  
    """
    Sends Given Sms To Given Mobile
    """
     # National SMS India
    request_url = "http://www.smsjust.com/blank/sms/user/urlsms.php?username=medicause&pass=@1!bE4gA&senderid=MEDCOJ&dest_mobileno={mobile}&message={message}&dltentityid=1201159835519074851&tmid=1602100000000004471&dltheaderid=1205163291379160291&dlttempid={temp_id}&response=Y"
    mobile = mobile[3:]
    message = '%2B'.join(message.split('+'))
    message = '%20'.join(message.split())
    link = request_url.format(mobile=mobile, message=message,temp_id=temp_id)
    if not settings.DEBUG:
        response=requests.get(link)
    else:
        print(link)
        # response=requests.get(link)
        # print(response)
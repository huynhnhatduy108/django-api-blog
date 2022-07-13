from datetime import datetime
import json
import re
import bcrypt
import random  
import string  
from slugify import slugify

salt = bcrypt.gensalt(10)
def gen_hash_password(password =''):
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    hashed = hashed.decode('utf-8')
    return hashed

def check_match_password(password, hash_password):
    if bcrypt.checkpw(password.encode('utf-8'), hash_password.encode('utf-8')):
        return True
    return False

def gen_slug(text):
    string_slug = slugify(text)
    return string_slug 

def gen_random_string(length = 5):
    string_code = ''.join((random.choice(string.ascii_lowercase + string.digits) for x in range(length)))
    return string_code

def gen_slug_radom_string(text, length = 5 ):
    string_slug = slugify(text)
    string_code = ''.join((random.choice(string.ascii_lowercase + string.digits) for x in range(length)))
    return string_slug + "-" + string_code

def now():
    return datetime.now()

def get_value_list(list, key):
    try:
        value_list = [obj[key] for obj in list]
        return value_list
    except Exception as e:
        return []

def compare_old_to_new_list(new_list=[] , old_list =[]):
    new_list = set([str(i) for i in new_list])
    old_list = set([str(i) for i in old_list])
    try:
        if new_list == old_list:
            return [], []
        else:
            list_add = list(new_list.difference(old_list))
            list_detele = list(old_list.difference(new_list))
            return list_add, list_detele
    except Exception as e:
        return [],[]  
     

def convert_to_dict(string, default={}):
    try:
        return json.loads(string)
    except:
        return default
        

def is_email_valid(email):
    pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'

    regex = re.compile(pattern)

    if email is None or (email is not None and regex.search(email)):
        return True
    else:
        return False
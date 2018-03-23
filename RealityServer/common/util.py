def oid_transform(my_dict):
    for x, y in my_dict.items():
        y['_id'] = str(y['_id'])


def oid_transform_search_dic(my_dict):
    for x, y in my_dict.items():
        y['_id'] = str(y['_id'])
        y['fake'] = 0
        if y['title'].startswith('詹皇反对'):
            y['clickbait'] = 1
        y['clickbait'] = 0


def oid_transform_list(my_list):
    for x in my_list:
        x['_id'] = str(x['_id'])


def data_success(data):
    return {'resultCode': 1, 'data': data}


def data_fail(message):
    return {'resultCode': 0, 'resultMessage': message}


def post_success():
    return {'resultCode': 1}


import bson


def bytes_to_str(obj):
    for key in obj:
        if type(obj[key]) is bytes:  # or type(obj[key]) is bson.binary.Binary):
            obj[key] = (obj[key].decode())
        if type(obj[key]) is bson.binary.Binary:
            obj[key] = bson.BSON(obj[key])
    return obj

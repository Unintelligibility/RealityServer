def oid_transform(my_dict):
    for x, y in my_dict.items():
        y['_id'] = y['_id']['$oid']


def data_success(data):
    return {'resultCode': 1, 'data': data}


def data_fail(message):
    return {'resultCode': 0, 'resultMessage': message}


import bson


def bytes_to_str(obj):
    for key in obj:
        if type(obj[key]) is bytes:  # or type(obj[key]) is bson.binary.Binary):
            obj[key] = (obj[key].decode())
        if type(obj[key]) is bson.binary.Binary:
            obj[key] = bson.BSON(obj[key])
    return obj

def oid_transform(my_dict):
    for x, y in my_dict.items():
        y['_id'] = y['_id']['$oid']


def data_success(data):
    return {'resultCode': 1, 'data': data}


def data_fail(message):
    return {'resultCode': 0, 'resultMessage': message}

def oid_transform(my_dict):
    for x, y in my_dict.items():
        y['_id'] = y['_id']['$oid']
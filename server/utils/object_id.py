from bson import ObjectId

def is_object_id(value):
    try:
        object_id = ObjectId(value)
        return True, object_id
    except Exception as e:
        return False, None
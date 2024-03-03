import uuid

def is_valid_uuid(value):
    try:
        uuid_obj = uuid.UUID(value)
        return True
    except ValueError:
        return False

def gen_question_id_for_list(data: list):
    for i in range(len(data)):
        uniqueId = str(uuid.uuid4())
        try:
            if not is_valid_uuid(data[i]["id"]):
                data[i]["id"] = uniqueId
        except Exception as e:
            data[i]["id"] = uniqueId
    return data
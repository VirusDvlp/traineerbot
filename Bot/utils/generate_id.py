import uuid


def generate_id() -> str:
    '''generating unique id for coach registration'''
    uid = uuid.uuid4()
    return str(uid)

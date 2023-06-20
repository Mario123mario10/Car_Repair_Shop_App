import uuid

def generate_unique_key(size=9):
    unique_key = str(uuid.uuid4().int)[:size]
    return unique_key
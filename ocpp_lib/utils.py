import random
import string


def random_message_id(length = 16) -> str:
    return "".join([random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length)])
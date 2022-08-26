import random
import string

from .models import URL_map


def get_unique_short_id():
    short_id = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(6)])
    if URL_map.query.filter_by(short=short_id).first() is not None:
        get_unique_short_id()
    return short_id

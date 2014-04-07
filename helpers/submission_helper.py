import base64
import uuid


def get_random_url_string():
    return base64.urlsafe_b64encode(uuid.uuid4().bytes)[:7]

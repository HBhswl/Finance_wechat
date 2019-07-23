import jwt
from datetime import datetime, timedelta
from finance.settings import SECRET_KEY
from users.models import Users


def create_token(user_id):
    payload = {
        'user_id': user_id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=30),
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256").decode()
    return token


def verify_token(token):
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except:
        return None
    if 'user_id' not in payload:
        return None
    try:
        user = Users.objects.get(pk=payload['user_id'])
    except Users.DoesNotExist:
        return None
    return user

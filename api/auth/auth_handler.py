import datetime
from typing import Dict

import jwt
from decouple import config

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")
TOKEN_LIFETIME = datetime.timedelta(seconds=600)

def token_response(token: str) -> Dict[str, str]:
    return {"access_token": token}

def encode_jwt(user_id: str) -> Dict[str, str]:
    payload = {
        "userId": user_id,
        "exp": datetime.datetime.utcnow() + TOKEN_LIFETIME
    }
    token = jwt.encode(payload=payload, key=JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)

def decode_jwt(token: str) -> Dict[str, str]:
    try:
        decoded_token = jwt.decode(jwt=token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token
    except jwt.ExpiredSignatureError:
        # TODO error code
        return {}
    except:
        return {}
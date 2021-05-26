import jwt
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer

from . import auth_handler

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        self.verify_jwt(credentials.credentials)
        return credentials
    
    def verify_jwt(self, token: str):
        try:
            payload = auth_handler.decode_jwt(token=token)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Expired authorization token")
        except:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authorization token")
        return bool(payload)

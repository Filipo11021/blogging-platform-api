from typing import Optional
from fastapi import Security, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
import string
import random

def secret_generator(size=30, chars=string.digits + string.ascii_letters):
    return ''.join(random.choice(chars) for _ in range(size))

class Auth():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    SECRET = os.getenv('AUTH_SECRET', secret_generator(30))
    ALGORITHM = "HS256"

    @classmethod
    def get_password_hash(cls, password:str):
        return cls.pwd_context.hash(password)
    
    @classmethod
    def verify_password(cls, plain_password:str, hashed_password:str):
        return cls.pwd_context.verify(plain_password, hashed_password)
    
    @classmethod
    def encode_token(cls, user_id:int, exp_time:Optional[timedelta] = None):
        if not exp_time:
            exp_time = timedelta(days=1)
        payload = {
            'exp': datetime.utcnow() + exp_time,
            'iat': datetime.utcnow(),
            'user_id': user_id
        }
        encoded_jwt = jwt.encode(
            payload,
            cls.SECRET,
            algorithm=cls.ALGORITHM
        )
        return encoded_jwt
    
    @classmethod
    def decode_token(cls, token):
        try:
            payload = jwt.decode(token, cls.SECRET, algorithms=cls.ALGORITHM)
            user_id = payload['user_id']
            
            if user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid')
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='expired')
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid')
    
    @classmethod
    def auth_wrapper(cls, auth:HTTPAuthorizationCredentials = Security(security)):
        return cls.decode_token(auth.credentials)
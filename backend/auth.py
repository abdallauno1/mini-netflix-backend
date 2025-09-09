import os, time, jwt
from passlib.context import CryptContext
SECRET_KEY=os.getenv('JWT_SECRET','dev-secret-change-me')
ALGORITHM='HS256'
ACCESS_TOKEN_EXPIRE_SECONDS=int(os.getenv('JWT_TTL_SECONDS','3600'))
pwd_context=CryptContext(schemes=['bcrypt'], deprecated='auto')
def hash_password(p): return pwd_context.hash(p)
def verify_password(p,h): return pwd_context.verify(p,h)
def create_access_token(sub:str)->str:
    now=int(time.time()); payload={'sub':sub,'iat':now,'exp':now+ACCESS_TOKEN_EXPIRE_SECONDS}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
def decode_token(t:str)->dict:
    return jwt.decode(t, SECRET_KEY, algorithms=[ALGORITHM])

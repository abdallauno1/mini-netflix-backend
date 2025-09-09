from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .database import Base, engine, SessionLocal
from .models import User, Movie
from .auth import hash_password, verify_password, create_access_token, decode_token
app=FastAPI(title='Mini Netflix Backend', version='0.1.0')
security=HTTPBearer()
@app.on_event('startup')
def on_startup():
    Base.metadata.create_all(bind=engine)
    db=SessionLocal()
    try:
        if db.query(Movie).count()==0:
            db.add_all([Movie(title='The Matrix', year=1999),Movie(title='Inception', year=2010),Movie(title='Interstellar', year=2014),Movie(title='The Dark Knight', year=2008)])
            db.commit()
    finally:
        db.close()
class SignupRequest(BaseModel):
    username:str
    password:str
class LoginRequest(BaseModel):
    username:str
    password:str
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(creds: HTTPAuthorizationCredentials=Depends(security), db: Session=Depends(get_db)):
    token=creds.credentials
    try:
        payload=decode_token(token); username=payload.get('sub')
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
    user=db.query(User).filter(User.username==username).first()
    if not user:
        raise HTTPException(status_code=401, detail='User not found')
    return user
@app.get('/health')
def health(): return {'status':'ok'}
@app.post('/signup')
def signup(req:SignupRequest, db:Session=Depends(get_db)):
    if db.query(User).filter(User.username==req.username).first():
        raise HTTPException(status_code=400, detail='Username already exists')
    user=User(username=req.username, password_hash=hash_password(req.password))
    db.add(user); db.commit(); return {'message':'user created'}
@app.post('/login')
def login(req:LoginRequest, db:Session=Depends(get_db)):
    user=db.query(User).filter(User.username==req.username).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    token=create_access_token(user.username); return {'access_token':token, 'token_type':'bearer'}
@app.get('/me')
def me(current=Depends(get_current_user)):
    return {'username': current.username}
@app.get('/movies')
def movies(current=Depends(get_current_user), db:Session=Depends(get_db)):
    return [{'id':m.id,'title':m.title,'year':m.year} for m in db.query(Movie).all()]

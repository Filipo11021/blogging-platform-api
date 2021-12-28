from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Depends
from sqlalchemy.orm.session import Session
from . import crud, models, schemas
from .database import engine, get_db
from .auth import Auth
from typing import List

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.post('/register')
def write_user(user:schemas.UserCreate, db:Session = Depends(get_db)):
    new_user = crud.create_user(db, user)
    token = Auth.encode_token(new_user.id)
    return {'token': token}
    
@app.post('/login')
def login_user(user: schemas.UserLogin, db:Session = Depends(get_db)):
    token = crud.get_token(db, user)
    return {'token': token}

@app.post('/posts')
def write_post(
    post:schemas.PostCreate, 
    db:Session = Depends(get_db), 
    payload = Depends(Auth.auth_wrapper)
):
    return crud.create_post(
        db=db, 
        post=post, 
        user_id=payload['user_id'] )

@app.get('/posts', response_model=List[schemas.Post])
def read_posts(db:Session = Depends(get_db), skip:int = 0, limit:int = 100):
    return crud.get_posts(
        db=db, 
        skip=skip, 
        limit=limit )

@app.get('/posts/{post_id}', response_model=schemas.Post)
def read_post(post_id:int, db:Session = Depends(get_db)):
    return crud.get_post_by_id(db=db, post_id=post_id)

@app.delete('/posts/{post_id}')
def remove_post(
    post_id:int, 
    db:Session = Depends(get_db), 
    payload = Depends(Auth.auth_wrapper)
):
    return crud.delete_post(
        db=db, 
        post_id=post_id, 
        user_id=payload['user_id'] )

@app.put('/posts/{post_id}')
def update_post(
    post:schemas.PostCreate, 
    post_id:int, 
    db:Session = Depends(get_db),
    payload = Depends(Auth.auth_wrapper)
):
    return crud.update_post(
        db=db, 
        post_id=post_id, 
        user_id=payload['user_id'], 
        post=post )
    
@app.get('/users/{users_id}/posts', response_model=List[schemas.Post])
def read_user_posts(user_id:int, db:Session = Depends(get_db), skip:int = 0, limit:int = 100):
    return crud.get_posts(
        db=db, 
        user_id=user_id, 
        skip=skip, 
        limit=limit )

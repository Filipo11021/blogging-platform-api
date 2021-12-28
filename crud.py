from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from fastapi import status
from .auth import Auth
from . import models, schemas 

def create_user(db:Session, user: schemas.UserCreate):
    hashed_password = Auth.get_password_hash(user.password)
    db_user = models.User(email = user.email, username = user.username, password = hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_token(db:Session, user: schemas.UserLogin):
    check_user = get_user(db, user)
    if (not check_user) or (not Auth.verify_password(user.password, check_user.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid username and/or password'
        )
    token = Auth.encode_token(check_user.id)
    return token

def get_user(db:Session, user:schemas.UserLogin):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    return db_user

def create_post(db:Session, post: schemas.PostCreate, user_id:int):
    new_post = models.Post(**post.dict(), author_id = user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def get_post_by_id(db:Session, post_id:int):
    print(post_id)
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    return post

def delete_post(db:Session, post_id: int, user_id: int):
    print('delete', post_id, user_id)
    post = db.query(models.Post).filter(models.Post.id == post_id, models.Post.author_id == user_id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    print(post)
    post.delete()
    db.commit()
    return {"detail": "deleted"}

def get_posts(db:Session, skip: int=0, limit:int=100, user_id:int=None):
    posts = db.query(models.Post)
    if user_id:
        posts = posts.filter(models.Post.author_id == user_id)
    posts_data = posts.offset(skip).limit(limit).all()
    return posts_data

def update_post(db:Session, post_id:int, user_id:int, data:schemas.PostCreate):
    print('postid', post_id, 'userid', user_id)
    post = db.query(models.Post).filter(
        models.Post.id == post_id,
        models.Post.author_id == user_id
    )
    post_data = post.first()
    if not post_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='not found'
        )
    post.update({**data.dict()})
    db.commit()
    return post.first()
    

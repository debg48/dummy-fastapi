from fastapi import FastAPI,HTTPException,status,Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from . import models
from .database import SessionLocal,engine
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Post(BaseModel):
    title : str 
    content : str 
    published : bool = True

try:
    conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='1234',cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database Connection Successful!")
    
except Exception as e :
    print(str(e))

#test route
@app.get('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data":posts}

@app.post("/posts")
def create_post(post : Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",(post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id : int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found !")
    return {"data":post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found !")
    return {"data":deleted_post}

@app.put("/posts/{id}")
def update_post(id :int, post : Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s ,published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found !")
    return{"data": updated_post}


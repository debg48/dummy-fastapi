from fastapi import FastAPI,HTTPException,status,Depends
# import psycopg2
# from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from . import models
from .database import engine,get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title : str 
    content : str 
    published : bool = True

# try:
#     conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='',cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print("Database Connection Successful!")
    
# except Exception as e :
#     print(str(e))

#test route
# @app.get('/sqlalchemy')
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"status": "success" , "data" : posts}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data":posts}

@app.post("/posts")
def create_post(post : Post,db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",(post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
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


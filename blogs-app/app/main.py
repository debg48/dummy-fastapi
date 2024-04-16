from fastapi import FastAPI,HTTPException,status
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title : str 
    content : str 
    published : bool = True

try:
    conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='',cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database Connection Successful!")
    
except Exception as e :
    print(str(e))
    
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


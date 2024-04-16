from fastapi import FastAPI
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


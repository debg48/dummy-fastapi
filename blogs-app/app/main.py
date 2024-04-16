from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

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


from fastapi import FastAPI
from fastapi.responses import HTMLResponse

posts: list[dict] = [
    {
        "id":1,
        "author":"corey schafer",
        "title":"fastapi is awesome",
        "content":"this framework is really easy to work with and super fast",
        "date_posted":"April 20, 2025",
    },
    {
        "id":2,
        "author":"John doe",
        "title":"python is great for web development",
        "content":"python is a greate language for web development, and fastapi makes it even better",
        "date_posted":"April 21, 2025",
    }
]

app = FastAPI()

@app.get("/")
def home():
    return {"message":"Hello wor!"}

@app.get('/api/posts')
def get_posts():
    return posts
from fastapi import FastAPI

from typing import Any, Dict

from .dummy_data import posts, users
from api.model import PostSchema

app = FastAPI()

@app.get("/", tags=["root"])
async def read_root() -> Dict[str, str]:
    return {"message": "Hello, World!"}

@app.get("/posts", tags=["posts"])
async def get_posts() -> Dict[str, Any]:
    return {"data": posts}

@app.get("/posts/{id}", tags=["posts"])
async def get_one_post(id: int) -> Dict[str, Any]:
    for post in posts:
        if post.get("id") == id:
            return {"data": post}
    else:
        return {"error": f"No such post with Id={id}."}

@app.post("/posts", tags=["posts"])
async def add_post(post: PostSchema) -> Dict[str, Any]:
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {
        "data": "post successfully added"
    }
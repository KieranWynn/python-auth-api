from fastapi import FastAPI, Body, Depends

from typing import Any, Dict

from .dummy_data import posts, users
from api.model import PostSchema, UserSchema, UserLoginSchema
from api.auth import auth_handler, auth_bearer

app = FastAPI()

def check_user_login(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False


@app.get("/", tags=["root"])
async def read_root() -> Dict[str, str]:
    return {"message": "Hello, World!"}

@app.post("/user/register", tags=["user"])
async def register_user(user: UserSchema = Body(...)) -> Dict[str, str]:
    users.append(user) # replace with db call, making sure to hash the password first
    return auth_handler.encode_jwt(user_id=user.email)

@app.post("/user/login", tags=["user"])
async def login_user(user: UserLoginSchema = Body(...)) -> Dict[str, str]:
    if check_user_login(user):
        return auth_handler.encode_jwt(user_id=user.email)
    return {
        "error": "incorrect login details"
    }

@app.post("/user/logout", tags=["user"])
async def logout_user(userId: str = Body(...)) -> Dict[str, str]:
    return {
        "data": "user successfully logged out"
    }

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

@app.post("/posts", dependencies=[Depends(auth_bearer.JWTBearer())], tags=["posts"])
async def add_post(post: PostSchema) -> Dict[str, Any]:
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {
        "data": "post successfully added"
    }
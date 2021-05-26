from pydantic import BaseModel, Field, EmailStr

class UserSchema(BaseModel):
    full_name: str = Field()
    email: EmailStr = Field()
    password: str = Field()

    class Config(object):
        schema_extra = {
            "example": {
                "full_name": "Kieran Wynn",
                "email": "kieran.wynn@example.com",
                "password": "weakpassword1234"
            }
        }


class UserLoginSchema(BaseModel):
    email: EmailStr = Field()
    password: str = Field()

    class Config(object):
        schema_extra = {
            "example": {
                "email": "kieran.wynn@example.com",
                "password": "weakpassword1234"
            }
        }


class PostSchema(BaseModel):
    id: int = Field(default=None)
    title: str = Field()
    content: str = Field()

    class Config(object):
        schema_extra = {
            "example": {
                "title": "Securing FastAPI applications with JWT.",
                "content": "In this tutorial, you'll learn how to secure your application by enabling authentication using JWT. We'll be using PyJWT to sign, encode and decode JWT tokens."
            }
        }
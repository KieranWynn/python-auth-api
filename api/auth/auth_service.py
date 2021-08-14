from .auth_models import UserInDB
from . import auth_helpers

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$nOwwjtjyleDLMJB7iivNSu7Kq8GE59PRxI2tV.Pmfwv0M6v75exWC",
        "disabled": False,
    }
}


async def get_user(username: str, db=fake_users_db) -> UserInDB:
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


async def get_authenticated_user(username: str, password: str, db=fake_users_db) -> UserInDB:
    user = await get_user(username, db=db)
    if not user:
        return False
    if not auth_helpers.verify_password(password, user.hashed_password):
        return False
    return user
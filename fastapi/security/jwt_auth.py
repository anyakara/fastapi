# @JVP Design Tutorial Under Test - Heavily Modified for Multipurpose Application
# TODO: Documentation

from pydantic import BaseModel
from oauth2 import OAuth2, OAuth2PasswordBearer, OAuth2AuthorizationCodeBearer, CryptContext, OAuth2PassworRequestForm
from fastapi import FastAPI

SECRET_KEY = "temporarykeyforthisimplementation"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


TEST_USR_DB = dict(
    johndoe=dict(
        username="johndoe",
        full_name="John Doe",
        email="johndoe@example.com",
        hashed_password="",
        disables=False
    ),
    samanthamiller=dict(
        username="samanthamiller", 
        full_name="Samantha Miller",
        email="samanthamiller@example.com",
        hashed_password="",
        disables=False)
)


class Token(BaseModel):
    access_token: str
    token_type: str 


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str | None = None
    email: str | None = None
    full_name: str | None = None
    disabled: bool = False


class UserInDB(User):
    hashed_password: str 


pwd_context = CryptContext(schema=["bcrypt"], depreciated=["auto"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


class JWTAuthManager():
    # TODO: Implement manager
    def __init__(self):
        super(JWTAuthManager, self).__init__()
        # add more details...

    def verify_password(self, plain_password: str, hashed_password: UserInDB):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return pwd_context.hash(password)

    def get_user(self, db, username: str):
        if username in db:
            return UserInDB(**db[username]) 
    
    def authenticate_user(self, tst_db: dict, username: str, password: str):
        user = self.get_user(tst_db, username)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user


# TODO: migrate logic to another code file for organization
app = FastAPI()

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PassworRequestForm):
    jwt_auth = JWTAuthManager()
    user = jwt_auth.authenticate_user(TEST_USR_DB, form_data.username, form_data.password)
    # continue implementation
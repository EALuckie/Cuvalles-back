#secureAuth.py

#Import dependencies
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from databases.database import SearchUser

#Initialize router instance
router= APIRouter()
#Authentication instance
oauth2= OAuth2PasswordBearer(tokenUrl="login") #As argument, the url of where the authentication is made
#ALGORITHM
ALGORITHM= "HS256"
#Context
crypt= CryptContext(schemes=["bcrypt"])
#Token's duration
ACCESS_TOKEN_DURATION= 1
#SECRET: openssl rand -hex 32
SECRET= "eeac39f760d3308b2d9b14461bb80c5c8ead88744039c33c826aa0dd7afb5528"

#Models for users
class User(BaseModel):
    username: str #Most be changed to iD
    email: str
#
class UserDB(User):
    password: str

def search_user_db(username: str):
    users_db= SearchUser(username)
    if username in users_db:
        return UserDB(**users_db[username])
    
#Dependence criteria
async def current_user(token: str= Depends(oauth2)):
    user= search_user(token)
    if not user: 
        raise HTTPException(
                                status_code=status.HTTP_401_UNAUTHORIZED,
                               detail="Password not correct",
                               headers={"www-Authenticate":"Bearer"}
                               )                           
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm= Depends()):
    user_db= search_user_db(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="User doesn't match")
    #
    user= search_user_db(form.username)
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    #

    access_token= {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    }
    #
    return {"access_token": jwt.encode(access_token, SECRET,algorithm=ALGORITHM), "token_type":"bearer"}

@router.get("users/me")
async def me(user: User= Depends(current_user)):
    pass

@router.get("/secure/status")
async def status():
    return {"Secure users status":"Congrats is working"}
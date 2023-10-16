#basic_auth_users.py
"""
Autentication for users:
    Sure you wanna have users in your app,
so this is what it is for.
"""

#Import libraries
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from databases.database import SearchUser

#Create our instance
router= APIRouter()
#Authentication instance
oauth2= OAuth2PasswordBearer(tokenUrl="login") #As argument, the url of where the authentication is made

#We need a Database, but we'll create a class instead
class User(BaseModel):
    username:str
    email: str
#
class UserDB(User):
    password: str


def search_user_db(username: str):
    users_db= SearchUser(username)
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    users_db= SearchUser(username)
    if username in users_db:
        return User(**users_db[username])
    
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
    
@router.post("/login2")
async def login(form: OAuth2PasswordRequestForm= Depends()):
    #Depends means we'll receive data, but that doesn't depends on someone
    user_db= search_user_db(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="User doesn't match")
    #
    user= search_user_db(form.username)
    if not form.password== user.password:
        raise HTTPException(status_code=400, detail="Incorrect password")
    #
    return {"access_token":user.username, "token_type":"bearer"}

@router.get("/users/me2")
async def me(user: User= Depends(current_user)):
    return user

@router.get("/users/status")
async def status():
    return {"Users status":"Congrats is working"}
#users.py

"""
Functionalities?
- Add user
- User login

What else?
"""

#Import libraries and modules
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from databases.database import SearchUser

#Create our router instance
router= APIRouter()
#Authentication instance
oauth2= OAuth2PasswordBearer(tokenUrl="login") #As argument, the url of where the authentication is made

#The user needed for login
class User(BaseModel):
    id: int
    email: str

#The user as it is in Database
class UserDB(User):
    password: str

def search_user(id: int):
    user= SearchUser(id)
    if id != None:
        return UserDB(**user[id]) #iD, email, password

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
async def user_login(form: OAuth2PasswordRequestForm= Depends()):
    user_db= SearchUser(form.id)
    if user_db== None:
        raise HTTPException(
            status_code= 400, detail= "User not found"
        )
        #return {"SearchUser error" : "User not found"}
    else:
        user= search_user(form.id) #iD, email, password
    #
    if not form.password == user.password:
        raise HTTPException(
            status_code=400, detail="La contraseña no es correcta"
        )
    return {"access_token":user.id , "token_type":"bearer"}

@router.get("/users/me")
async def me(user: User= Depends(current_user)):
    return user

@router.get("/status/login")
async def status():
    return "Its working"

"""
Hash and veryfy the password:

Authentication is the process of verifying users before granting
them access to secure reosurces.
Then a user is authenticatied, they're allowed to access these secured resourcecs.

"""
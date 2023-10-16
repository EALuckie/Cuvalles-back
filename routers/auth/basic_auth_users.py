#basic_auth_users.py
#This may be deleted
"""
Autentication for users:
    Sure you wanna have users in your app,
so this is what it is for.
"""

#Import libraries
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

#Create our instance
app= FastAPI()
#Authentication instance
oauth2= OAuth2PasswordBearer(tokenUrl="login") #As argument, the url of where the authentication is made

#Access the real DB
def SearchUser(id: int):
    try:
        cursor= connection.cursor()
        #Model SQL
        sql=f"SELECT * FROM `Usuarios` WHERE iD_Usuarios={id};"
        cursor.execute(sql)
        records = cursor.fetchall()
        connection.commit()
        return {records[0][0]:{"id":records[0][0],"email":records[0][5],"password":records[0][1]}}
    except:
        {"SearchUser() error":"User not found"}

#We need a Database, but we'll create a class instead
class User(BaseModel):
    id: int
    email: str
#
class UserDB(User):
    password: str

"""We cannot have in full display the password, the pw is stored in DB"""
users_db= {
    "Sheshe": {
        "username": "SheshEGM",
        "full_name": "Ernesto Luckie",
        "email": "ernesto@gmail.com",
        "disabled": False,
        "password": "123456" #In DB this must be encrypted, how?
    },
    "Sheshe2": {
        "username": "SheshEGM2",
        "full_name": "Ernesto Luckie2",
        "email": "ernesto2@gmail.com",
        "disabled": False,
        "password": "123456" #In DB this must be encrypted, how?
    }
}

def search_user(id: int):
    n= SearchUser()
    if n != None:
        return UserDB(**n[id])
    
#Dependence criteria
async def current_user(token: str= Depends(oauth2)):
    user= search_user(token)
    if not user: 
        raise HTTPException(
                                status_code=status.HTTP_401_UNAUTHORIZED,
                               detail="Password not correct",
                               headers={"www-Authenticate":"Bearer"}
                               )
    if user.disabled:
        raise HTTPException(
                                status_code=status.HTTP_401_UNAUTHORIZED,
                               detail="Usere inacitve",
                               headers={"www-Authenticate":"Bearer"}
                               )
    return user
    
@app.post("/login")
async def login(form: OAuth2PasswordRequestForm= Depends()):
    #Depends means we'll receive data, but that doesn't depends on someone
    user_db= SearchUser(form.id)
    if not user_db:
        raise HTTPException(status_code=400, detail="User doesn't match")
    #
    user= search_user(form.id)
    if not form.password== user.password:
        raise HTTPException(status_code=400, detail="Incorrect password")
    #
    return {"access_token":user.username, "token_type":"bearer"}

@app.get("/users/me")
async def me(user: User= Depends(current_user)):
    return user
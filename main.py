#main.py
#Running on kallen's environment

#Import libraries
from routers.auth import basicAuth, secureAuth
from fastapi import FastAPI
from routers.auth import users
#Insert here API for database

#Initialize main instance
app= FastAPI()

#Routers and resources
app.include_router(basicAuth.router)
app.include_router(secureAuth.router)

@app.get("/")
async def root():
    return "Hola desde el backend"

#Documentation on Swagger: http://127.0.0.1:8000/docs
#Documentation on Redocly: http://127.0.0.1:8000/redoc

#Inicia el servidor: uvicorn main:app --reload
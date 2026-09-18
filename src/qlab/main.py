from fastapi import FastAPI
from qlab.core.model import test_user

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/user")
async def user():
    return {"message": "sucess", "data": test_user}
 

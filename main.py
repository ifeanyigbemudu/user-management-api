from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import user_collection
from bson import ObjectId
import hasher as hsh
import schema as sch

app = FastAPI()

#Schema
class User(BaseModel):
    email: str
    password: str
    logged_in: bool = False

#Get users
@app.get("/list-users")
async def list_users():
    users = sch.users_serializer(user_collection.find())
    return {"status": "ok", "data": users}


#Register user
@app.post("/register")
async def register(user: User):
    user.password = hsh.hash_password(user.password)
    x = user_collection.insert_one(dict(user))
    user = sch.user_serializer(user_collection.find_one({"_id": x.inserted_id}))
    return {"status": "ok", "data": user}

#Delete user
@app.post("/delete/{user_id}")
async def delete_user(user_id):
    now_user = user_collection.find_one_and_delete({"_id": ObjectId(user_id)})
    if now_user:
        return {"status": "ok", "data": f"User has been deleted"}
    else:
        raise HTTPException(404, "User was not found")

#Sign in
@app.post("/sign-in")
async def sign_in(user: User):
    now_user = sch.user_serializer(user_collection.find_one({"email": user.email}))
    if now_user:
        is_correct = hsh.check_password(user.password, now_user["password"])
        if is_correct:
            user_collection.find_one_and_update({"email": user.email}, {"$set": {"logged_in": True}})
            return {"status": "ok", "data": user.email+" is now logged in"}
        else:
            raise HTTPException(404, f"Yo! That password no go work.")
    else:
        raise HTTPException(404, f"{user.email} does not exist in our database.")
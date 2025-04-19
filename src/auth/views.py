from contextvars import Token
import os,requests
from dotenv import load_dotenv
from fastapi import APIRouter,Depends,HTTPException,Request,Response,Form
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import RedirectResponse
from database import gets
from sqlalchemy.orm import Session
from src.auth.schema import TokenResponse
from src.auth.utils import token_creator
from src.auth.manager import verify_password
from src.auth.manager import upsert_user
from src.auth.schema import NewUser,LoginDetails
from database.models.user import UserTable 
from fastapi.responses import JSONResponse
from fastapi import Security

from fastapi.openapi.models import OAuthFlows, OAuthFlowPassword
from datetime import datetime, timezone
load_dotenv()

auth_router=APIRouter()
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="auth/login")

@auth_router.post("/login",response_model=TokenResponse)
async def login(
    username:str=Form(...),
    password:str=Form(...),
    db:Session=Depends(gets.get_db)
):
    user=db.query(UserTable).filter(UserTable.username==username).first()
    user.last_logged_in=datetime.now(timezone.utc)
    db.commit()

    if not user:
        raise HTTPException(status_code=401,detail="User not found")

    if not verify_password(password,user.password):
        raise HTTPException(status_code=401,detail="Invalid password")

    token,user_data=await token_creator({
        "user_id":str(user.user_id),
        "email":user.email
    },db)

    return JSONResponse({
        "access_token":token,
        "token_type":"bearer",
        "username":user_data['username'],
        "user_id":user_data['user_id']
    },status_code=200)


@auth_router.get("/protected_route")
async def protected_route(
    token:str=Security(oauth2_scheme)
):
    return {"message":"You are authenticated","token":Token}



@auth_router.post("/signup")
async def signup(userDetails:NewUser,db:Session=Depends(gets.get_db)):
    existing_email=db.query(UserTable).filter(UserTable.email==userDetails.email).first()
    if existing_email:
        raise HTTPException(status_code=409,detail="Email already exists")

    existing_username = db.query(UserTable).filter(UserTable.username == userDetails.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")

    user_data = {
        "name": userDetails.name,
        "username": userDetails.username,
        "email": userDetails.email,
        "password": userDetails.password,
        "created_at": datetime.now(timezone.utc),
        "last_logged_in": datetime.now(timezone.utc),
        "is_active": True,
        "role": "developer"
    }
    user_data=await upsert_user(user_data,db)
    return JSONResponse(content={
        "username": user_data['username'],
        "user_id": user_data['user_id'],
        "last_logged_in": user_data['last_logged_in']
    }, status_code=200)


    


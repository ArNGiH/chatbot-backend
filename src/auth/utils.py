import base64
from datetime import datetime,timezone,timedelta
import hashlib
import os
from typing import Optional
from dotenv import load_dotenv
from fastapi import HTTPException
from jose import jwt 
from requests import Session
from src.auth.manager import upsert_user

load_dotenv()
PRIVATE_KEY=os.getenv("PRIVATE_KEY")

async def create_access_token(user_data: dict, expires_delta: Optional[timedelta] = None):
    '''Function to create Custom JWT access token based on the user data payload'''
    to_encode = user_data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=720)

    to_encode.update({"exp": int(expire.timestamp())})  
    to_encode["user_id"] = str(to_encode["user_id"])
    to_encode["email"] = str(to_encode["email"])

    encoded_jwt = jwt.encode(to_encode, PRIVATE_KEY, algorithm="HS256")
    return encoded_jwt

async def token_creator(user_data,db:Session):
    try:
        user_data=await upsert_user(user_data,db)
    except Exception as e :
        raise HTTPException(status_code=500,detail=str(e))

    try:
        jwt_token = await create_access_token(user_data)
    except Exception as e:
        raise HTTPException(status_code=401,detail=str(e))

    return jwt_token,user_data

import os
from dotenv import load_dotenv
from fastapi import HTTPException,Header,status
from jose import JWTError,jwt,ExpiredSignatureError

load_dotenv()

PRIVATE_KEY=os.getenv("PRIVATE_KEY")

async def verify_token(app_token:str=Header(...)):
    """
    Verify the JWT token and return the payload
    Returns the decoded payload of the user in a dictionary.
    """
    try:
        payload=jwt.decode(app_token,PRIVATE_KEY,algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")


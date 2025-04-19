import datetime
from sqlalchemy.orm import Session
from database.models.user import UserTable as User

from passlib.context import CryptContext
pwd_context=CryptContext(schemes=["sha256_crypt"],deprecated="auto")

def hash_password(password:str)->str:
    return pwd_context.hash(password)

def verify_password(password:str,hashed_password:str)->bool:
    return pwd_context.verify(password,hashed_password)

class MyException(Exception):
    pass

async def upsert_user(user_data:dict,db:Session):
    try:
        existing_user=db.query(User).filter(User.email==user_data["email"]).first()

        if existing_user:
            print("Existing user")
            existing_user.last_logged_in=datetime.datetime.now(datetime.timezone.utc)
            db.commit()
            db.refresh(existing_user)
            user_obj=existing_user
        else:
            print("New user")
            new_user=User(
                name=user_data["name"],
                email=user_data["email"],
                username=user_data["username"],
                created_at=datetime.datetime.now(datetime.timezone.utc),
                last_logged_in=datetime.datetime.now(datetime.timezone.utc),
                password=hash_password(user_data["password"]),
                is_active=True,
                role=user_data["role"]
            
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            user_obj=new_user

        return {
            "user_id": str(user_obj.user_id),  # Ensure UUID is a string
            "name": user_obj.name,
            "username": user_obj.username,
            "email": user_obj.email,
            "created_at": user_obj.created_at.isoformat(),  # Ensure datetime is a string
            "last_logged_in": user_obj.last_logged_in.isoformat()
        }
    except Exception as e:
        db.rollback()
        raise MyException("Unable to upsert user",{e})



async def get_user_data_from_email(token_data:dict,db:Session):
    current_user_data=db.query(User).filter(User.email==token_data["email"]).first()
    if not current_user_data:
        raise Exception("User does not exist in the database")

    return current_user_data.__dict__


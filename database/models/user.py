from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from database.settings import Base
import uuid

class UserTable(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    
    role = Column(String, nullable=False, default="developer")  
    is_active = Column(Boolean, nullable=False, default=True)   

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    last_logged_in = Column(DateTime, nullable=False, server_default=func.now())

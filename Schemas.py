from pydantic import BaseModel
from typing import Optional

from sqlalchemy.sql.functions import current_date

class CreateHod(BaseModel):
    name: str
    email: str
    phone_num: int
    user_name: str
    department: str

class ShowHods(CreateHod):
    class Config():
        orm_mode = True

class AdminPass(BaseModel):
    username: str
    current_pass: str
    new_pass: str

class Admin(BaseModel):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    admin: Optional[str] = None


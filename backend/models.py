from pydantic import BaseModel, EmailStr


class User(BaseModel):
    name: str
    email: EmailStr
    family_name: str
    given_name: str
    email_verified: bool

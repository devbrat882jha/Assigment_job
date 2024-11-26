
from pydantic import BaseModel,field_validator,model_validator,EmailStr,ValidationInfo
from models import UserRole



def validate_non_empty_string(value:str,field):
    if not value.strip():
        raise ValueError(f" {field} cannot be empty")
    return value

class UserSignupInput(BaseModel):
    name:str
    email: EmailStr
    password:str
    confirm_password:str
    role:UserRole

    @field_validator('name')
    @classmethod
    def validate_name(cls, value, info:ValidationInfo):
        return validate_non_empty_string(value, info.field_name)
    
    @model_validator(mode='after')
    def check_password_match(self):
         pw1 = self.password
         pw2 = self.confirm_password
         if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('passwords do not match')
         return self
    


class LoginInput(BaseModel):
    email:str
    password:str

    @field_validator('password')
    @classmethod
    def validate_password(cls, password,info:ValidationInfo):
        return validate_non_empty_string(value=password,field=info.field_name)


class JobCreate(BaseModel):
    title: str
    description: str
   
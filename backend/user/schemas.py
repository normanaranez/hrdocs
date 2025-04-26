from ninja import Schema

class LoginSchema(Schema):
    username: str
    password: str

class RegisterSchema(Schema):
    username: str
    password: str
    email: str

class UserSchema(Schema):
    id: int
    username: str
    email: str
    # Add other fields you want to expose

class LogoutSchema(Schema):
    refresh: str
    # Add other fields you want to expose
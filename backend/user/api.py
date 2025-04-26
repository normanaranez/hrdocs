from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI
from ninja_jwt.authentication import JWTAuth
from django.contrib.auth import get_user_model, authenticate
from .schemas import LoginSchema, RegisterSchema, UserSchema, LogoutSchema
from ninja.errors import HttpError
from ninja_jwt.tokens import RefreshToken

api = NinjaExtraAPI()

api.register_controllers(NinjaJWTDefaultController)

# Get the custom user model
User = get_user_model()

@api.post("/login")
def login(request, payload: LoginSchema):
    """
    Login user and return JWT token.
    """
    user = authenticate(username=payload.username, password=payload.password)
    if not user:
        raise HttpError(401, "Invalid username or password")
    
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

# @api.post("/logout", auth=JWTAuth())
# def logout(request, payload: LogoutSchema):
#     """
#     Logout user by blacklisting the refresh token.
#     """
#     try:
#         token = RefreshToken(payload.refresh)
#         if token:
#             token.blacklist()
#         return {"success": True}
#     except Exception as e:
#         raise HttpError(400, str(e))
    
# @api.post("/logout-all", auth=JWTAuth())
# def logout_all(request):
#     """
#     Logout user from all devices by blacklisting all refresh tokens.
#     """
#     try:
#         user = request.user
#         for token in RefreshToken.objects.filter(user=user):
#             token.blacklist()
#         return {"success": True}
#     except Exception as e:
#         raise HttpError(400, str(e))

@api.post("/register")
def register(request, payload: RegisterSchema):
    """
    Register a new user and return JWT token.
    """
    if User.objects.filter(username=payload.username).exists():
        raise HttpError(400, "Username already exists")
    
    user = User.objects.create_user(
        username=payload.username,
        password=payload.password,
        email=payload.email,
    )
    
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }

@api.get("/current-user", response=UserSchema, auth=JWTAuth())
def current_user(request):
    print('test', request)
    user = request.user
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        # Add other fields you want to expose
    }


from fastapi import APIRouter, Depends, Cookie
from fastapi.responses import JSONResponse
from starlette.requests import Request
from models import User
from auth import get_current_user

# global route collection
api_router = APIRouter(default_response_class=JSONResponse)

public_routes = APIRouter()
authenticated_routes = APIRouter()
user_router = APIRouter()


@public_routes.get("/pub")
def g():
    return "ok2"


@user_router.get("/")#, response_model=User)
def f(req: Request, user=Depends(get_current_user)):
    # print(req.headers)
    # return user
    return user


authenticated_routes.include_router(
    user_router, prefix='/user', tags=['User']
)

api_router.include_router(
    public_routes
)

api_router.include_router(
    authenticated_routes,
    # dependencies=[]
)

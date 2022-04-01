from fastapi import FastAPI, Cookie
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

from routes import api_router

app = FastAPI(
    title="some name",
    debug=True,
    swagger_ui_init_oauth={
        # If you are using pkce (which you should be)
        "usePkceWithAuthorizationCodeGrant": True,
        # Auth fill client ID for the docs with the below value
        "clientId": "swagger-client-id-for-dev",  # example-frontend-client-id-for-dev
        "scopes": {}
    }
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root(req: Request):
    print(req.query_params)
    print(req.cookies)
    print(req.path_params)
    print(req.query_params)
    return {"message": "Hello World"}

app.include_router(api_router)

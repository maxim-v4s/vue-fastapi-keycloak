from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi import Security, HTTPException, status, Depends
from pydantic import Json
from models import User
from keycloak.keycloak_openid import KeycloakOpenID

protocol = "http"
host = "keycloak"
port = 8080
realm = "entropy_hub"  # example-realm
server_url = f"{protocol}://{host}:{port}/"
authorization_url = f"{server_url}realms/{realm}/protocol/openid-connect/auth"
client_id = "fastapi-client"  # backend-client-id
# TODO: change to real secret
client_secret = "XCfGZJCK2sbBHFUdDIELQ3DLUnX"  # your backend client secret
token_url = f"{server_url}realms/{realm}/protocol/openid-connect/token"

# This is just for fastapi docs
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=authorization_url,
    tokenUrl=token_url,
)

# This actually does the auth checks
keycloak_openid = KeycloakOpenID(
    server_url=server_url,
    client_id=client_id,
    realm_name=realm,
    # client_secret_key=client_secret,
    # TODO: change to True when use signed certificates
    verify=True
)


async def get_idp_public_key():
    print("try get public key")
    cert = (
        "-----BEGIN PUBLIC KEY-----\n"
        f"{keycloak_openid.public_key()}"
        "\n-----END PUBLIC KEY-----"
    )
    print("success get public key")
    return cert


async def get_auth(token: str = Security(oauth2_scheme)) -> Json:
    try:
        return keycloak_openid.decode_token(
            token,
            key=await get_idp_public_key(),
            options={
                "verify_signature": True,
                "verify_aud": False,
                "exp": True
            }
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),  # "Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    identity: Json = Depends(get_auth)
): #-> User:
    # print(type(identity), identity)
    return identity #User(**identity)
    # return User.first_or_fail(identity['sub']) # get your user form the DB using identity['sub']

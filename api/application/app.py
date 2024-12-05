import os

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from keycloak import KeycloakOpenID
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

# Конфигурация CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Конфигурация Keycloak
KEYCLOAK_SERVER_URL = os.getenv("KEYCLOAK_SERVER_URL")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")
KEYCLOAK_ALLOWED_ROLE = os.getenv("KEYCLOAK_ALLOWED_ROLE")

# Инициализация Keycloak клиента
keycloak_openid = KeycloakOpenID(
    server_url=KEYCLOAK_SERVER_URL,
    client_id=KEYCLOAK_CLIENT_ID,
    realm_name=KEYCLOAK_REALM
)

# Проверка разрешений
def verify_permissions(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    token = credentials.credentials
    
    try:
        decoded_token = keycloak_openid.decode_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    roles = decoded_token.get("realm_access", {}).get("roles", [])
    if "prothetic_user" not in roles:
        raise HTTPException(status_code=401, detail="Not enough permissions")


@app.get("/reports", status_code=200)
async def get_reports(_=Depends(verify_permissions)):
    return "Data report"
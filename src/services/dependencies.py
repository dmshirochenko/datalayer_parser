import os
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

bearer_scheme = HTTPBearer()


def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if credentials.scheme != "Bearer":
        raise HTTPException(status_code=403, detail="Invalid scheme")
    if credentials.credentials != os.getenv("BEARER_TOKEN"):
        raise HTTPException(status_code=403, detail="Invalid token")
    return credentials



from fastapi import Cookie, HTTPException, Depends
from jwt import ExpiredSignatureError, PyJWTError, decode
from datetime import datetime
from src.config.security import settings
from typing import Optional

def get_current_user(access_token: Optional[str] = Cookie(default=None)):
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = decode(access_token, settings.secret_key, algorithms=[settings.algorithm])

        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"user_id": user_id, "token_payload": payload}

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Access token expired")

    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid access token")

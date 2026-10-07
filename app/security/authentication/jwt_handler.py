import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv


load_dotenv()


SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError(
        "JWT_SECRET_KEY is not set in the environment"
    )

ALGORITHM = "HS256"


def create_access_token(
    user_id: str,
    role: str,
    expires_minutes: int = 60,
) -> str:

    now = datetime.now(timezone.utc)

    payload = {
        "sub": user_id,
        "role": role,
        "iat": now,
        "exp": now + timedelta(
            minutes=expires_minutes
        ),
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def verify_access_token(token: str) -> dict:

    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )
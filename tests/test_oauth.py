from jose import jwt
from datetime import datetime, timezone

import pytest

from app.routers.oauth import create_app_jwt


@pytest.mark.asyncio
async def test_me_returns_user(client_factory):
    async with client_factory() as client:
        r = await client.get("/oauth/me")

    assert r.status_code == 200
    assert r.json() == {"email": "test@test.com"}


def test_create_app_jwt_contains_email_and_exp(test_env):
    token = create_app_jwt("user@test.com")

    payload = jwt.decode(
        token,
        test_env["APP_JWT_SECRET"],
        algorithms=["HS256"]
    )

    assert payload["sub"] == "user@test.com"
    assert "exp" in payload


def test_jwt_exp_in_future(test_env):
    token = create_app_jwt("user@test.com")

    payload = jwt.decode(
        token,
        test_env["APP_JWT_SECRET"],
        algorithms=["HS256"]
    )

    exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    assert exp > datetime.now(tz=timezone.utc)

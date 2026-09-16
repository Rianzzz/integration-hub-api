from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from integration_hub.core.config import get_settings
from integration_hub.core.security import create_access_token
from integration_hub.domain.exceptions import InvalidCredentialsError

router = APIRouter(tags=["auth"])


@router.post("/auth/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> dict[str, str]:
    settings = get_settings()
    if form_data.username != settings.api_username or form_data.password != settings.api_password:
        raise InvalidCredentialsError("Usuário ou senha incorretos")

    token = create_access_token(subject=form_data.username)
    return {"access_token": token, "token_type": "bearer"}

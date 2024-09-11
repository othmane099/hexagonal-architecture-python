from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.sms.core.domain.dtos import LoginResponseDTO
from src.sms.core.exceptions import InvalidCredential
from src.sms.core.ports.services import AuthenticationService

router = APIRouter()


@router.get("/ping")
def ping():
    return {"success": True, "message": "Pong!"}


@router.post("/token")
@inject
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    authentication_service_impl: AuthenticationService = Depends(
        Provide["authentication_service_impl"]
    ),
) -> LoginResponseDTO:
    try:
        login_response = await authentication_service_impl.authenticate(form_data)
    except InvalidCredential as e:
        raise HTTPException(
            status_code=404, detail=str(e), headers={"WWW-Authenticate": "Bearer"}
        )
    return login_response

from dependency_injector.wiring import Provide

from src.sms.core.domain.dtos import (UserResponseDTO,
                                      convert_user_to_user_response_dto)
from src.sms.core.exceptions import EntityNotFound
from src.sms.core.ports.services import UserService
from src.sms.core.ports.unit_of_works import UserUnitOfWork


class UserServiceImpl(UserService):

    def __init__(
        self, user_unit_of_work: UserUnitOfWork = Provide["user_unit_of_work"]
    ):
        self.user_unit_of_work = user_unit_of_work

    async def find_by_username(self, username: str) -> UserResponseDTO:
        async with self.user_unit_of_work as uow:
            user = await uow.repository.find_by_username(username)
            if not user:
                raise EntityNotFound("User not found with given username")
            return convert_user_to_user_response_dto(user)

from dependency_injector.wiring import Provide

from src.sms.core.domain.dtos import (UserResponseDTO,
                                      convert_user_to_user_response_dto)
from src.sms.core.exceptions import EntityNotFound
from src.sms.core.ports.services import UserService
from src.sms.core.ports.unit_of_works import UnitOfWork


class UserServiceImpl(UserService):

    def __init__(self, unit_of_work: UnitOfWork = Provide["unit_of_work"]):
        self.unit_of_work = unit_of_work

    async def find_by_username(self, username: str) -> UserResponseDTO:
        async with self.unit_of_work as uow:
            user = await uow.user_repository.find_by_username(username)
            if not user:
                raise EntityNotFound("User not found with given username")
            return convert_user_to_user_response_dto(user)

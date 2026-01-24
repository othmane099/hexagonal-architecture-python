from src.sms.core.domain.models import Role
from src.sms.core.ports.repositories import RoleRepository


class FakeRoleRepository(RoleRepository):

    def __init__(
        self,
        roles: list[Role] | None = None,
        role_permissions: dict[str, list[str]] | None = None,
    ):
        self._roles: list[Role] = roles if roles is not None else []
        self._role_permissions: dict[str, list[str]] = (
            role_permissions if role_permissions is not None else {}
        )

    async def find_by_name(self, name: str) -> Role | None:
        for role in self._roles:
            if role.name == name and role.deleted_at is None:
                return role
        return None

    async def role_has_permission(self, role_name: str, permission_name: str) -> bool:
        permissions = self._role_permissions.get(role_name, [])
        return permission_name in permissions

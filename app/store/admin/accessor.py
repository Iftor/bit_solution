import typing
from hashlib import sha256
from typing import Optional

from app.admin.utils import hash_password
from app.base.base_accessor import BaseAccessor
from app.admin.models import Admin

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application"):
        first_admin_data = self.app.config.admin
        await self.create_admin(
            email=first_admin_data.email,
            password=first_admin_data.password
        )

    async def get_by_email(self, email: str) -> Optional[Admin]:
        admin_list = list(
            filter(
                lambda admin: admin.email == email,
                self.app.database.admins
            )
        )
        return admin_list[0] if admin_list else None

    async def create_admin(self, email: str, password: str) -> Admin:
        self.app.database.admins.append(
            admin := Admin(
                id=self.app.database.next_admin_id,
                email=email,
                password=hash_password(password)
            )
        )
        return admin

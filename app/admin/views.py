from aiohttp.web_exceptions import HTTPForbidden, HTTPUnauthorized
from aiohttp_apispec import request_schema
from aiohttp_session import new_session

from app.admin.schemes import AdminRequestSchema, AdminResponseSchema
from app.admin.utils import check_password
from app.web.app import View
from app.web.utils import json_response


class AdminLoginView(View):
    @request_schema(AdminRequestSchema)
    async def post(self):
        email = self.data["email"]
        password = self.data["password"]

        manager_data = await self.store.admins.get_by_email(email)
        if not manager_data:
            raise HTTPForbidden

        if not check_password(manager_data.password, password):
            raise HTTPForbidden

        session = await new_session(self.request)
        raw_manager_data = AdminResponseSchema().dump(manager_data)
        session["manager_data"] = raw_manager_data

        return json_response(data=raw_manager_data)


class AdminCurrentView(View):
    async def get(self):
        if not (manager_data := self.request.admin):
            raise HTTPUnauthorized
        return json_response(data=AdminResponseSchema().dump(manager_data))

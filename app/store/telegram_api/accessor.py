import random
import typing
from typing import Optional

from aiohttp import TCPConnector
from aiohttp.client import ClientSession

from app.base.base_accessor import BaseAccessor
from app.store.vk_api.dataclasses import Message, Update, UpdateObject, UpdateMessage

if typing.TYPE_CHECKING:
    from app.store.vk_api.poller import Poller
    from app.web.app import Application


class VkApiAccessor(BaseAccessor):
    class Constants:
        API_VERSION = "5.131"
        VK_API_HOST = "https://api.vk.com/method/"
        GET_LONG_POLL_SERVER_METHOD = "groups.getLongPollServer"
        MESSAGE_SEND_METHOD = "messages.send"
        MESSAGE_NEW_TYPE = "message_new"

    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.session: Optional[ClientSession] = None
        self.key: Optional[str] = None
        self.server: Optional[str] = None
        self.poller: Optional[Poller] = None
        self.ts: Optional[int] = None

    async def connect(self, app: "Application"):
        from app.store.vk_api.poller import Poller

        self.session = ClientSession(connector=TCPConnector(verify_ssl=False))
        await self._get_long_poll_service()
        self.poller = Poller(self.app.store)
        await self.poller.start()

    async def disconnect(self, app: "Application"):
        if self.session and not self.session.closed:
            await self.session.close()
        if self.poller and self.poller.is_running:
            await self.poller.stop()

    def _build_query(self, host: str, method: str, params: dict) -> str:
        url = host + method + "?"
        if "v" not in params:
            params["v"] = self.Constants.API_VERSION
        url += "&".join([f"{k}={v}" for k, v in params.items()])
        return url

    async def _get_long_poll_service(self):
        url = self._build_query(
            host=self.Constants.VK_API_HOST,
            method=self.Constants.GET_LONG_POLL_SERVER_METHOD,
            params={
                "access_token": self.app.config.bot.token,
                "group_id": self.app.config.bot.group_id,
            }
        )
        async with self.session.get(url) as response:
            data = (await response.json())["response"]
            self.key = data["key"]
            self.server = data["server"]
            self.ts = data["ts"]

    async def poll(self) -> list[Update]:
        url = self._build_query(
            host=self.server,
            method="",
            params={
                "act": "a_check",
                "key": self.key,
                "ts": self.ts,
                "wait": 25,
            }
        )
        async with self.session.get(url) as response:
            data = await response.json()
            self.ts = data["ts"]
            updates = [
                Update(
                    type=self.Constants.MESSAGE_NEW_TYPE,
                    object=UpdateObject(
                        message=UpdateMessage(
                            from_id=update["object"]["message"]["from_id"],
                            text=update["object"]["message"]["text"],
                            id=update["object"]["message"]["id"],
                        )
                    )
                ) for update in data.get("updates", [])
                if update["type"] == self.Constants.MESSAGE_NEW_TYPE
            ]
        return updates

    async def send_message(self, message: Message) -> None:
        url = self._build_query(
            host=self.Constants.VK_API_HOST,
            method=self.Constants.MESSAGE_SEND_METHOD,
            params={
                "user_id": message.user_id,
                "message": message.text,
                "access_token": self.app.config.bot.token,
                "random_id": random.randint(1, 123453423)
            }
        )

        async with self.session.get(url):
            pass

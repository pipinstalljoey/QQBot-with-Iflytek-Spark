# -*- coding: utf-8 -*-
import asyncio
import os
import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import Message, DirectMessage
import AskAndAnswer

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_at_message_create(self, message: Message):
        _log.info(message.author.avatar)
        if "sleep" in message.content:
            await asyncio.sleep(10)
        _log.info(message.author.username)
        await message.reply(content=f"{AskAndAnswer.question(message.content)}")

    async def on_direct_message_create(self, message: DirectMessage):
        await self.api.post_dms(
            guild_id=message.guild_id,
            content=f"{AskAndAnswer.question(message.content)}",
            msg_id=message.id,
        )


if __name__ == "__main__":
    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_guild_messages=True, direct_message=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], token=test_config["token"])

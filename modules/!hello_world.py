import asyncio

name = "Hello world"
description = """
Example module

hi, hello: Sends 'Hello world!'
"""


async def OnReady(client, modules):
    print("Hello world!")


async def Hello(client, message):
    await message.channel.send("Hello world!")


functions = {
    "hello": Hello,
    "hi": Hello
}

import asyncio

name = "Hello world"
description = """
Example module

hi, hello: Sends 'Hello world!'
"""


async def OnReady(client):
    print("Hello world!")
    print(client.user.name + " is now ready! <3")


async def Hello(client, message):
    await message.channel.send("Hello world!")


functions = {
    "hello": Hello,
    "hi": Hello
}

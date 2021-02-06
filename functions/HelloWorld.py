import asyncio

name = "Hello world"
description = "Example function"
cmdsHelp = {
    "hi, hello": "Sends 'Hello world!'"
}


async def Ready(client):
    print("Hello world!")
    print(client.user.name + " is now ready! <3")


async def Call(client, message):
    if message.content[0] in ("hi", "hello"):
        await message.channel.send("Hello world!")
        return True

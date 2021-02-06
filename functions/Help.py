import asyncio
import json
import os
from threading import Timer

name = "Help"
description = "Function for displaying help"
cmdsHelp = {
    "functions": "prints all functions",
    "help *function*": "prints help for the function"
}

functionsString = ""
helpStrings = {}


async def Call(client, message):
    if message.content[0] == "functions":
        await message.channel.send(functionsString)
        return True

    elif message.content[0] == "help":
        func = " ".join(message.content[1:])
        await message.channel.send(helpStrings[func])
        return True


async def Ready(client):
    with open("functions-meta.json", "r", encoding="utf-8") as f:
        metaData = json.loads(f.read())

    global functionsString, helpStrings

    functionsString = ", ".join(metaData.keys())

    for func in metaData.keys():
        helpStrings[func.lower()] = "{}\n - {}\n{}".format(
            func, metaData[func]["description"], "\n".join(
                ["{}: {}".format(cmd, metaData[func]["cmdsHelp"][cmd]) for cmd in metaData[func]["cmdsHelp"].keys()]))

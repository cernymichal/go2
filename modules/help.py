import asyncio
import json
import os
from threading import Timer

name = "Help"
description = """
Module for displaying help

modules: prints all modules
help *module*: prints help for a Module
"""

metadata = {}


async def OnReady(client):
    global metadata
    with open("modules-meta.json", "r", encoding="utf-8") as f:
        metadata = json.loads(f.read())


async def Modules(client, message):
    await message.channel.send(", ".join(metadata.keys()))


async def Help(client, message):
    module = " ".join(message.content[1:])
    await message.channel.send(metadata[module]["description"])


functions = {
    "modules": Modules,
    "help": Help
}

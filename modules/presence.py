import asyncio
import discord

name = "Presence"
description = "Presence module"


async def OnReady(client, modules):
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name="Komm, süsser Tod"
        ),
        status=discord.Status.online
    )

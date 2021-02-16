import asyncio
from os import listdir
import discord

name = "Sound"
description = """
Plays sounds from folder

play *sound*: plays a sound
stop: stops
leave: leaves the voice channel
list: prints all available sounds
"""

soundsList = [i[:-4] for i in listdir("sounds")]


async def Play(client, message):
    message.content = " ".join(message.content[1:])
    if message.author.voice.channel == None:
        await message.channel.send("no vc")
    elif not message.content in soundsList:
        await message.channel.send("sorry don't have that")
    else:
        await Stop(client, message)

        vc = message.guild.voice_client
        if vc == None:
            vc = await message.author.voice.channel.connect()

        file = "sounds/{}.mp3".format(message.content)

        vc.play(discord.FFmpegPCMAudio(file))

        await message.channel.send("playing {}".format(message.content))


async def Stop(client, message):
    if message.guild.voice_client != None:
        message.guild.voice_client.stop()


async def List(client, message):
    await message.channel.send("\n".join(soundsList))


async def Disconnect(client, message):
    if message.guild.voice_client != None:
        await Stop(client, message)
        await message.guild.voice_client.disconnect()
        await message.channel.send("au revoir")


functions = {
    "play": Play,
    "stop": Stop,
    "leave": Disconnect,
    "list": List
}

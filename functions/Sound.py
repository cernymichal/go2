import asyncio
from os import listdir
import discord

name = "Sound"
description = "Plays sounds from folder"
cmdsHelp = {
    "play *sound*": "plays a sound",
    "stop": "stops",
    "leave": "leaves the voice channel",
    "list": "prints all available sounds"
}

voice_clients = {}  # server.id: player
soundsList = [i[:-4] for i in listdir("sounds")]


async def Call(client, message):
    if message.content[0] == "play":
        message.content = " ".join(message.content[1:])
        if message.author.voice.channel == None:
            await message.channel.send("no vc")
        elif not message.content in soundsList:
            await message.channel.send("not in sounds list")
        else:
            Stop(message.guild.id)
            await Play(message)
        return True

    elif message.content[0] == "stop":
        Stop(message.guild.id)
        return True

    elif message.content[0] == "leave":
        await Disconnect(message.guild.voice_client, message.guild.id)
        return True

    elif message.content[0] == "list":
        await List(message.channel)
        return True


async def Play(message):
    vc = message.guild.voice_client
    if vc == None:
        vc = await message.author.voice.channel.connect()

    vc.play(discord.FFmpegPCMAudio("sounds/{}.mp3".format(message.content)))

    voice_clients[message.guild.id] = vc


def Stop(guildID):
    if guildID in voice_clients.keys() and voice_clients[guildID].is_playing():
        voice_clients[guildID].stop()


async def List(channel):
    s = ""
    for sound in soundsList:
        s += sound+"\n"
    await channel.send(s)


async def Disconnect(vc, guildID):
    if guildID in voice_clients.keys() and vc != None:
        Stop(guildID)
        await vc.disconnect()
        del voice_clients[guildID]

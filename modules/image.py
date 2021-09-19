import asyncio
import os
import discord

name = "Image"
description = """
Posts images from folder

image *name*: posts image
images: lists all images
"""

folder = "images"

imageList = {}
for i in os.listdir(folder):
    imageList[os.path.splitext(i)[0]] = i


async def Image(client, message):
    message.content = " ".join(message.content[1:])
    if message.content not in imageList.keys():
        await message.channel.send("sorry don't have that")
    else:
        await message.channel.send(
            file=discord.File(os.path.join(folder, imageList[message.content]))
        )


async def List(client, message):
    await message.channel.send("\n".join(imageList))


functions = {
    "image": Image,
    "images": List
}

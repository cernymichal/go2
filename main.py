import discord
import asyncio
import json
import os

config = {
    "prefix": "",
    "functionsFolder": "",
    "token": ""
}
functions = []


def CreateConfig():
    prefix = input("prefix: ")
    functionsFolder = input("functionsFolder: ")
    token = input("token: ")

    config["prefix"] = prefix
    config["functionsFolder"] = functionsFolder
    config["token"] = token

    with open("config.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(config))


def LoadConfig():
    global config
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.loads(f.read())


def SaveFunctionMetaData():
    man = {}
    for func in functions:
        man[func.name] = {
            "description": func.description,
            "cmdsHelp": func.cmdsHelp
        }

    with open("functions-meta.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(man))


def AddFunctionsFromFolder(path):
    import sys
    sys.path.insert(0, path)

    for i in os.listdir(path):
        if os.path.isfile(os.path.join(path, i)) and i[-3:] == ".py" and i[0] != "!":
            i = i[:-3]
            exec("import {}".format(i))
            exec("functions.append({})".format(i))


client = discord.Client()


@client.event
async def on_ready():
    for func in functions:
        try:
            await func.Ready(client)
        except AttributeError:
            pass

    print("name: {}".format(client.user.name))
    print("id: {}".format(client.user.id))
    print("avatar: {}".format(client.user.avatar_url))
    print("guilds: {}".format(
        len(client.guilds) if len(client.guilds) > 10
        else str([guild.name for guild in client.guilds])[1:-1]
    ))
    print("functions: {}".format(str([func.name for func in functions])[1:-1]))
    print("\nready!\n")


@client.event
async def on_message(message):
    if message.content.lower().startswith(config["prefix"]):
        print('{} | {} >> "{}"'.format(
            message.guild.name, message.author, message.content))
        message.content = message.content.lower(
        )[len(config["prefix"]):].strip().split(" ")

        for func in functions:
            if await func.Call(client, message):
                break


if __name__ == '__main__':
    print(os.path.dirname(os.path.abspath(__file__)))
    if os.path.isfile("config.json"):
        LoadConfig()
    else:
        CreateConfig()

    AddFunctionsFromFolder(config["functionsFolder"])
    SaveFunctionMetaData()

    client.run(config["token"])

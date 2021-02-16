import discord
import asyncio
import json
import os

config = {
    "prefix": "",
    "modulesFolder": "",
    "token": ""
}
modules = []
functions = {}


def CreateConfig():
    config["prefix"] = input("prefix: ")
    config["modulesFolder"] = input("modules folder: ")
    config["token"] = input("token: ")

    with open("config.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(config))


def LoadConfig():
    global config
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.loads(f.read())


def AddModulesFromFolder(path):
    import sys
    sys.path.insert(1, path)

    for file in os.listdir(path):
        filePath = os.path.join(path, file)
        if os.path.isfile(filePath) and os.path.splitext(filePath)[-1] == ".py" and file[0] != "!":
            file = file[:-3]
            exec("import {}".format(file))
            exec("modules.append({})".format(file))

    global functions

    for module in modules:
        if hasattr(module, "functions"):
            functions = {**functions, **module.functions}


client = discord.Client()


@client.event
async def on_ready():
    for module in modules:
        try:
            await module.OnReady(client, modules)
        except AttributeError:
            pass

    print("modules: {}".format(", ".join([module.name if hasattr(module, "name") else module.__name__ for module in modules])))
    print("ready!\n")


@client.event
async def on_message(message):
    if message.content.lower().startswith(config["prefix"]):
        print('{} | {} >> "{}"'.format(
            message.guild.name, message.author, message.content))
        message.content = message.content[len(
            config["prefix"]):].strip().split(" ")

        try:
            await functions[message.content[0]](client, message)
        except KeyError:
            pass


if __name__ == '__main__':
    if os.path.isfile("config.json"):
        LoadConfig()
    else:
        CreateConfig()

    AddModulesFromFolder(config["modulesFolder"])

    client.run(config["token"])

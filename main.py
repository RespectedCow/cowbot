#!/usr/bin/python
# Discord bot for RespectedCow's servers.
# Import modules
from discord.ext import commands
 
TOKEN = open("token.txt", "r").readline()
client = commands.Bot(command_prefix = "$")
#answers with the ms latency
@client.command()
async def get(ctx):
    print(ctx)
 
client.run(TOKEN)
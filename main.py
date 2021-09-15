#!/usr/bin/python
# Discord bot for RespectedCow's servers.
# Import modules
import discord
from discord.ext import commands
import subprocess
import urllib.request
 
TOKEN = open("token.txt", "r").readline()
client = commands.Bot(command_prefix = "cowbot ")

# If someone wants the ip
@client.command(pass_context=True)
async def get(ctx, arg):
    if arg == "ip":
        # Get ip
        ip = subprocess.check_output(["curl", "ifconfig.co"])

        ip = str(ip)

        # Filter
        filterlist = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", "."]

        filtered = ""

        for i in list(ip):
            if i in filterlist:
                filtered = filtered + i


        await ctx.send("The ip is " + filtered + ":25565")
        print(filtered)
    else:
        await ctx.send("Unknown argument")

# validates server for ip update
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def validate(ctx, arg):
    if ctx.message.author.mention == discord.Permissions.administrator:
        if ctx.message != None:
            channel = discord.utils.get(ctx.guild.channels, name=arg)

            if channel != None:
                await ctx.send("Validated " + arg)
    else:
        await ctx.send("You don't have the perms to use this command!")
 
client.run(TOKEN)
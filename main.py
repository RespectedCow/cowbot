#!/usr/bin/python
# Discord bot for RespectedCow's servers.
# Import modules
import discord
from discord.ext import commands
import subprocess
import socket
 
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
    elif arg == "status":
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1',25565))
        if result == 0:
            await ctx.send("Server is open")
        else:
            await ctx.send("Server is closed")
        sock.close()
    elif arg == "commands":
        await ctx.send("""
        Commands are:
        status
        ip
        commands
        """)
    else:
        await ctx.send("Unknown argument")

# STarts the server
@client.command(pass_context=True)
async def start(ctx, arg):
    if arg == "server":
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1',25565))
        if result == 0:
            await ctx.send("Server is open")
        else:
            subprocess.call("cd ~/minecraft")
            subprocess.call("./minecraft.sh")

            await ctx.send("Server startup process has began")                 
    else:
        await ctx.send("Invalid argument")

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
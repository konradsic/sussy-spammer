import discord
from discord.ext import commands
import asyncio
import os
import datetime
import time
from dotenv import load_dotenv
import json

load_dotenv()
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

with open("./config.json", mode="r", encoding="utf-8") as f:
    data = json.load(f)

ALWAYS_ON_TARGET_ID = data["ALWAYS_ON_TARGET_ID"]
UPDATE_USER_ID = data["UPDATE_USER_ID"]
GUILD_ID = data["GUILD_ID"]

# embed
embed = data["embed"]
TITLE = embed["title"]
DESCRIPTION = embed["description"]
IMAGE_URL = embed["image_url"]
COLOR = embed["color"]

async def trolluj_grybera(amount, interval, location):
    print("Starting trolling process")
    guild = bot.get_guild(GUILD_ID)
    print(f"Guild name: {guild.name}")
    user = discord.utils.get(guild.members, id=ALWAYS_ON_TARGET_ID)
    update_channel = discord.utils.get(guild.members, id=UPDATE_USER_ID)
    id = user.id

    embed = discord.Embed(
        title=TITLE,
        timestamp=datetime.datetime.utcnow(),
        color=discord.Color.from_str(COLOR),
        description=DESCRIPTION.replace("<location>", location))
    embed.set_thumbnail(url=IMAGE_URL)
    username = bot.get_user(id)
    if username is not None:
        username = username.name
    else: username = id
    print(f"Sending {amount} messages to {username}, {amount} times with interval {interval}s")
    await update_channel.send(f"Sending {amount} messages to {username}, {amount} times with interval {interval}s")
    message = await update_channel.send("Progress will show up here!")
    start_time = time.time()

    for i in range(amount):
        try:
            await user.send(content="https://discord.gg/dMK2dtAt4Q", embed=embed)
            await asyncio.sleep(interval)
            if i%10 == 0:
                elapsed_time = time.time() - start_time
                per_operation = elapsed_time / (i+1)
                minutes_left = per_operation * (amount - i - 1) / 60
                print(f"Progress: [{i+1}/{amount} - {round((i+1)/amount*100, 2)}%] ETA {round(minutes_left, 2)}min (per-op: {round(per_operation, 2)}s)")
                try:
                    await message.edit(content=f"Progress: [{i+1}/{amount} - {round((i+1)/amount*100, 2)}%] ETA {round(minutes_left, 2)}min (per-op: {round(per_operation, 2)}s)")
                except:
                    print(f"Failed to send update message to discord channel")
        except:
            try:
                await message.edit(content=f"Failed to send messages to {username}!")
                print("Failed to send messages, waiting......")
            except:
                pass
    await message.edit(content=f"Finished sending messages to {username}!")

@bot.event
async def on_ready():
    print(f"Connected to discord, latency: {round(bot.latency*1000)}ms")
    print(f"    Logged in as {bot.user.name}")
    print("[!] Starting trolluj_grybera function")
    await trolluj_grybera(32767, 1.5, "Władysławowo")

@bot.command()
async def trolluj(ctx, id: int, amount: int, interval: float, *, location: str=None):
    user = discord.utils.get(ctx.guild.members, id=id)

    embed = discord.Embed(
        title=TITLE,
        timestamp=datetime.datetime.utcnow(),
        color=discord.Color(int(COLOR)),
        description=DESCRIPTION.replace("<location>", location))
    embed.set_thumbnail(url=IMAGE_URL)
    username = bot.get_user(id)
    if username is not None:
        username = username.name
    else: username = id
    print(f"Sending {amount} messages to {username}, {amount} times with interval {interval}s")
    await ctx.channel.send(f"Sending {amount} messages to {username}, {amount} times with interval {interval}s")
    message = await ctx.channel.send("Progress will show up here!")
    start_time = time.time()

    for i in range(amount):
        try:
            await user.send(content="https://discord.gg/dMK2dtAt4Q", embed=embed)
            await asyncio.sleep(interval)
            if i%10 == 0:
                elapsed_time = time.time() - start_time
                per_operation = elapsed_time / (i+1)
                minutes_left = per_operation * (amount - i - 1) / 60
                print(f"Progress: [{i+1}/{amount} - {round((i+1)/amount*100, 2)}%] ETA {round(minutes_left, 2)}min (per-op: {round(per_operation, 2)}s)")
                try:
                    await message.edit(content=f"Progress: [{i+1}/{amount} - {round((i+1)/amount*100, 2)}%] ETA {round(minutes_left, 2)}min (per-op: {round(per_operation, 2)}s)")
                except:
                    print(f"Failed to send update message to discord channel")
        except:
            try:
                await message.edit(content=f"Failed to send messages to {username}!")
                print("Failed to send messages, waiting......")
            except:
                pass
    await message.edit(content=f"Finished sending messages to {username}!")


bot.run(os.environ["BOT_TOKEN"])

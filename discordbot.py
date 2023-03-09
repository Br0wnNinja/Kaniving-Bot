import discord
from discord.ext import commands, tasks
from itertools import cycle
import random
import os
import asyncio
import json
import tracemalloc
import youtube_dl
from config import TOKEN

voice_client = None

tracemalloc.start()

client = commands.Bot(command_prefix="$", intents=discord.Intents.all())

client.remove_command("help")

bot_status = cycle(["$bothelp" , "Join the Tournament"])


@tasks.loop(seconds=2)
async def change_status():
    await client.change_presence(activity=discord.Game(next(bot_status)))

@client.event
async def on_ready():
    await client.tree.sync()
    print("Bot is connected!")
    change_status.start()



async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")

@client.event
async def on_guild_join(guild):
    with open("cogs/json/welcome.json", "r") as f:
        data = json.load(f)
    
    data[str(guild.id)] = {}
    data[str(guild.id)]["Channel"] = None
    data[str(guild.id)]["Message"] = None
    data[str(guild.id)]["AutoRole"] = None
    data[str(guild.id)]["ImageUrl"] = None
    
    with open("cogs/json/welcome.json", "w") as f:
        json.dump(data, f, indent=4)


@client.event
async def on_guild_remove(guild):
    with open("cogs/json/welcome.json", "r") as f:
        data = json.load(f)
         
    data.pop(str(guild.id))
    
    with open("cogs/json/welcome.json", "w") as f:
        json.dump(data, f, indent=4)
        

class SelfRoles(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Red", style=discord.ButtonStyle.red)
    async def red_color(self, ctx, Button: discord.ui.Button):
        red_role = discord.utils.get(ctx.guild.roles, name="Red")
        
        await ctx.user.add_roles(red_role)
        
    @discord.ui.button(label="Green", style=discord.ButtonStyle.green)
    async def green_color(self, ctx, Button: discord.ui.Button):
        green_role = discord.utils.get(ctx.guild.roles, name="Green")
        
        await ctx.user.add_roles(green_role)
    
    
    @discord.ui.button(label="Blurple", style=discord.ButtonStyle.blurple)
    async def blurple_color(self, ctx, Button: discord.ui.Button):
        blurple_role = discord.utils.get(ctx.guild.roles, name="Blurple")
        
        await ctx.user.add_roles(blurple_role)

@client.tree.command(name="selfroles", description="Give yourself a color role!")
async def self_role(ctx):
    await ctx.response.send_message(content="Click a button corresponding to the role color you want!", view=SelfRoles())   

thumbs_up = "👍"
thumbs_down = "👎"
user_asked_count = {}

thumbs_up = "👍"
thumbs_down = "👎"
user_asked_count = {}

@client.event
async def on_message(message):
    global user_asked_count
    if message.author == client.user:
        return

    if not isinstance(message.channel, discord.DMChannel):
        # Ignore messages in non-DM channels and allow other commands
        await client.process_commands(message)
        return

    if message.author.id in user_asked_count:
        if user_asked_count[message.author.id] > 2:
            await message.channel.send("You've already been asked if you need support multiple times. Please contact the staff if you need further assistance.")
            return
        else:
            user_asked_count[message.author.id] += 1
    else:
        user_asked_count[message.author.id] = 1

    support_msg_sent = False
    while not support_msg_sent:
        if message.author.id in user_asked_count and user_asked_count[message.author.id] == 1:
            support_msg = await message.channel.send("Do you need support?")
            await support_msg.add_reaction(thumbs_up)
            await support_msg.add_reaction(thumbs_down)
            user_asked_count[message.author.id] += 1
        else:
            support_msg_sent = True

    def check(reaction, user):
        return user == message.author and str(reaction.emoji) in [thumbs_up, thumbs_down]

    try:
        reaction, user = await client.wait_for('reaction_add', timeout=3600.0, check=check)

        if str(reaction.emoji) == thumbs_up:
            await message.channel.send("What's the reason for the support ticket?")
            problem = await client.wait_for('message', timeout=3600.0, check=lambda m: m.author == message.author and isinstance(m.channel, discord.DMChannel))
            server = client.get_guild(980680618541207602)  # replace SERVER_ID with your server ID
            category = discord.utils.get(server.categories, name="Support")  # replace "Support" with your desired category name
            channel_name = problem.content.replace(" ", "-")[:90]  # use problem as channel name, max length 90 characters
            channel = await server.create_text_channel(name=channel_name, category=category, overwrites={
                server.default_role: discord.PermissionOverwrite(read_messages=False),
                message.author: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                server.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                server.get_role(980680618620887057): discord.PermissionOverwrite(read_messages=True, send_messages=True),
            })
            await channel.send(f"{message.author.mention} and {server.get_role(980680618620887057).mention}, a support channel has been created for you.")
            await channel.send(f"{message.author.mention}: {problem.content}")
            await message.channel.send(f"Here is your support channel, support staff will be with you shortly: {channel.mention}")
            user_asked_count[message.author.id] = 0  # reset user_asked_count for this user
        elif str(reaction.emoji) == thumbs_down:
            await message.channel.send("Have a good day! Feel free to contact me or staff if you have any questions or concerns.")
            user_asked_count[message.author.id] = 0  # reset user_asked_count for this user
    except asyncio.TimeoutError:
        if message.author.id in user_asked_count:
            await message.channel.send("I'm sorry, you took too long to react.")
            user_asked_count[message.author.id] = 0  # reset user_asked_count for this user






async def main():
    async with client:
        await load()
        await client.start(TOKEN)


asyncio.run(main())


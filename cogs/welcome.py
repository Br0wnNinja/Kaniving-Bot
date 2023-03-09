import discord 
from discord.ext import commands
import json

class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Welcome.py is ready!")
        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open("cogs/json/welcome.json", "r") as f:
            data = json.load(f)
        
        welcome_embed = discord.Embed(title=f"Welcome to {member.guild.name}!", description=f"Welcome to the server! You are member {member.guild.member_count}!", color=discord.Color.purple())
        
        welcome_embed.add_field(name="Welcome to the server!", value=data[str(member.guild.id)]["Message"], inline=False)
        welcome_embed.set_image(url=data[str(member.guild.id)]["ImageUrl"])
        welcome_embed.set_footer(text="Glad you're here!", icon_url=member.avatar)
        
        auto_role = discord.utils.get(member.guild.roles, name=data[str(member.guild.id)]["Autorole"])
        
        await member.add_roles(auto_role)
        
        if data[str(member.guild.id)]["Channel"] is None:
            await member.send(embed=welcome_embed)
        elif data[str(member.guild.id)]["Channel"] is not None:
            
            welcome_channel = discord.utils.get(member.guild.channels, name=data[str(member.guild.id)]["Channel"])
            
            await welcome_channel.send(embed=welcome_embed)
            
            
        
        
    @commands.group(name = "welcome", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def welcome(self, ctx):
        
        info_embed = discord.Embed(title="Welcome System Setup", description="Create a unqiue welcome system for the server!", color = discord.Color.blurple())
        info_embed.add_field(name = "autorole", value="Set an automatic role so when a user joins they will recieve it automatically", inline=False)
        info_embed.add_field(name = "message", value="Set a message to be included in the welcome card", inline=False)
        info_embed.add_field(name = "channel", value="Set a channel for the welcome card to appear", inline=False)
        info_embed.add_field(name = "img", value="Set an image of gif url to be sent with the welcome card", inline=False)
        
        await ctx.send(embed = info_embed)
        
    @welcome.command()
    @commands.has_permissions(administrator=True)
    async def autorole(self, ctx, role: discord.Role):
        with open("cogs/json/welcome.json", "r") as f:
            data = json.load(f)
        
        data[str(ctx.guild.id)]["AutoRole"] = str(role.name)
        
        with open("cogs/json/welcome.json", "w") as f:
            json.dump(data, f, indent=4)
    
    @welcome.command()
    @commands.has_permissions(administrator=True)
    async def message(self, ctx, *, msg):
        with open("cogs/json/welcome.json", "r") as f:
            data = json.load(f)
        
        data[str(ctx.guild.id)]["Message"] = str(msg)
        
        with open("cogs/json/welcome.json", "w") as f:
            json.dump(data, f, indent=4)
            
    @welcome.command()
    @commands.has_permissions(administrator=True)
    async def channel(self, ctx, channel: discord.TextChannel):
        with open("cogs/json/welcome.json", "r") as f:
            data = json.load(f)
        
        data[str(ctx.guild.id)]["Channel"] = str(channel.name)
        
        with open("cogs/json/welcome.json", "w") as f:
            json.dump(data, f, indent=4)
            
    @welcome.command()
    @commands.has_permissions(administrator=True)
    async def img(self, ctx, *, url):
        with open("cogs/json/welcome.json", "r") as f:
            data = json.load(f)
        
        data[str(ctx.guild.id)]["ImageUrl"] = str(url)
        
        with open("cogs/json/welcome.json", "w") as f:
            json.dump(data, f, indent=4)

async def setup(client):
    await client.add_cog(Welcome(client))
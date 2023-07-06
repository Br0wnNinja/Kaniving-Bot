import discord
from discord.ext import commands

class MapBan(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("MapBan.py is ready!")
        
    @commands.command()
    @commands.has_role("Staff")
    async def gameday(self, ctx, *args):
        ticket_info = " ".join(args)
        guild = ctx.guild
        
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        } 
        
        category = discord.utils.get(guild.categories, name="Gameday Tickets")
        
        if category is None:
            category = await guild.create_category("Gameday Tickets")
        
        ticket_name = ticket_info.split(":")[0].strip()
        ticket_mentions = " ".join([user.mention for user in ctx.message.mentions])
        ticket_message = f"**Ticket Name:** {ticket_name}\n**Users:** {ticket_mentions}"
        
        overwrites.update({user: discord.PermissionOverwrite(read_messages=True) for user in ctx.message.mentions})
        
        gameday_channel = await guild.create_text_channel(ticket_name.replace(" ", "-"), category=category, overwrites=overwrites)
                
        await gameday_channel.send(ticket_message)
        await gameday_channel.send("Please schedule your game and map bans within this channel!")
        await ctx.send("Ticket created successfully!")

async def setup(client):
    await client.add_cog(MapBan(client))

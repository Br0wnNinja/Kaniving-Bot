import discord 
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderation.py is ready!")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, count: int):
        await ctx.channel.purge(limit=count)
    
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, modreason):
        await ctx.guild.kick(member)

        conf_embed = discord.Embed(title="success!", color=discord.Color.green())
        conf_embed.add_field(name="kicked: ", value=f'{member.mention} has been kicked from the server by {ctx.author.mention}.', inline=False)
        conf_embed.add_field(name="Reason:", value=modreason, inline=False)

        await ctx.send(embed=conf_embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, modreason):
        await ctx.guild.ban(member)

        conf_embed = discord.Embed(title="success!", color=discord.Color.green())
        conf_embed.add_field(name="banned: ", value=f'{member.mention} has been banned from the server by {ctx.author.mention}.', inline=False)
        conf_embed.add_field(name="Reason:", value=modreason, inline=False)

        await ctx.send(embed=conf_embed)

    @commands.command(name="unban")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, userId):
        user = discord.Object(id=userId)
        await ctx.guild.unban(user)
        



async def setup(client):
    await client.add_cog(Moderation(client))
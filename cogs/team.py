import discord
from discord.ext import commands

class Teams(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Team.py is ready!")

    @commands.command()
    async def create(self, ctx, team_name: str, *team_members: discord.Member):
        """Create a new team with the specified name and add the specified members"""
        # Create the role with the specified name
        role_name = team_name.replace(" ", "_")
        role = await ctx.guild.create_role(name=role_name)

        # Add the specified members to the role
        for member in team_members:
            await member.add_roles(role)

        # Add the user who invoked the command to the role
        await ctx.author.add_roles(role)

        # Give the user who invoked the command the Team Captain role
        team_captain_role = discord.utils.get(ctx.guild.roles, name="Team Captain")
        await ctx.author.add_roles(team_captain_role)

        # Send a confirmation message
        member_mentions = " ".join(member.mention for member in team_members)
        confirmation_message = f"Created team {team_name} with members {member_mentions}. {ctx.author.mention} has been assigned as the team captain!"
        await ctx.send(confirmation_message)





async def setup(client):
   await client.add_cog(Teams(client))
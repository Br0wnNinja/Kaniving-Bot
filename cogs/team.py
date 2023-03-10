import discord
from discord.ext import commands

class Teams(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Team.py is ready!")

    @commands.command()
    async def create(self, ctx, *team_name: str, team_members: commands.Greedy[discord.Member]):
        """Create a new team with the specified name and add the specified members"""
        team_name = " ".join(team_name) # Combine all words into a single string
        # Create the role with the specified name
        role = await ctx.guild.create_role(name=team_name)

        # Add the specified members to the role
        for member in team_members:
            await member.add_roles(role)

        # Add the user who invoked the command to the role
        await ctx.author.add_roles(role)

        # Give the user who invoked the command the Team Captain role
        team_captain_role = discord.utils.get(ctx.guild.roles, name="Team Captain")
        await ctx.author.add_roles(team_captain_role)

        # Send a confirmation message
        await ctx.send(f"Created team {team_name} with members {', '.join(member.mention for member in team_members)}")


async def setup(client):
   await client.add_cog(Teams(client))
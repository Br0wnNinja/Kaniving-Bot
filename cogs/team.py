import discord
from discord.ext import commands
import csv

class TeamManagement(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Team Managment is ready!")

    @commands.command()
    @commands.has_role("Staff Team")  # Requires user to have the "Staff Team" role to run the command
    async def create(self, ctx, *, team_name_members: str):
        """Create a new team with the specified name and add the specified members"""
        # Separate the team name from the mentioned teammates using a dash
        team_name, mentioned_members = team_name_members.split("-")
    
        # Create the role with the specified name
        role_name = team_name.replace(" ", " ")
        role = await ctx.guild.create_role(name=role_name)

        # Add the specified members to the role
        mentioned_members = mentioned_members.strip().split(" ")
        team_members = []
        for member in mentioned_members:
            try:
                member_obj = await commands.MemberConverter().convert(ctx, member)
                team_members.append(member_obj)
                await member_obj.add_roles(role)
            except commands.errors.MemberNotFound:
                pass

        # Add the first mentioned user to the Team Captain role
        team_captain_role = discord.utils.get(ctx.guild.roles, name="Team Captains")
        if team_captain_role is not None:
            for member in team_members:
                if member != ctx.author:
                    await member.add_roles(team_captain_role)
                    team_captain_name = member.display_name
                    break

            # Send a confirmation message
            user_mention = ctx.author
            user_name = ctx.author.display_name
            team_members_names = [member.display_name for member in team_members if member != ctx.author]
            team_members_name_str = ", ".join(team_members_names)
            member_mentions = " ".join(member.mention for member in team_members if member != ctx.author)
            team_captain = next((member for member in team_members if member != ctx.author), None)
            team_captain_mention = team_captain.mention if team_captain else "None"
            confirmation_message = f"Created team {team_name} with members {member_mentions}. Team Captain role given to {team_captain_mention}. By {user_mention.mention}!"
            await ctx.send(confirmation_message)
            
            #Write to CSV file
            with open("team_data.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([team_name, team_members_name_str, team_captain_name, user_name])
            
        else:
            await ctx.send("Error: 'Team Captains' role not found.")
            
            
        
async def setup(client):
    await client.add_cog(TeamManagement(client))


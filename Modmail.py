import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True  # Ensure members intent is enabled
intents.message_content = True
intents.dm_messages = True  # Enable DMs

bot = commands.Bot(command_prefix="\\", intents=intents)

# IDs of roles that should receive modmail (replace with actual IDs)
MANAGER_ROLE_ID = 'MANAGER-ID' #<---------------- Replace with manager role ID
MOD_ROLE_ID = 'MOD-ID' #<-------------------- Replace with moderator role ID
OWNER_ROLE_ID = 'OWNER-ID' #<------------------ Replace with owner role ID
YOUR_GUILD_ID = 'SERVER-ID' # <----------------Replace with your server's ID

@bot.event
async def on_ready(): 
    print(f'Logged in as {bot.user}')   

@bot.event 
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel) and not message.author.bot:
        print(f"Received DM from {message.author}: {message.content}")

        # Check for greetings and mentions
        if message.content.lower() == "hi" or bot.user.mentioned_in(message):
            embed = discord.Embed(
                title="Welcome to Modmail",
                description=f"Hello {message.author.mention}! I'm Modmail. Write your query here and I will send it to the server owner and stafff team of our server.",
                color=discord.Color.blue()
            )
            await message.author.send(embed=embed)
            return

        # For other messages, treat them as queries
        try:
            confirmation_embed = discord.Embed(
                title="Query Send!",
                description="Your query has been successfully sent to the server owner and our server staff team.",
                color=discord.Color.green()
            )
            await message.author.send(embed=confirmation_embed)

            # Forward the query to server roles
            guild = bot.get_guild(YOUR_GUILD_ID)
            if guild is None:
                print("Guild not found")
                return

            print("Guild found:", guild.name)

            manager_role = guild.get_role(MANAGER_ROLE_ID)
            mod_role = guild.get_role(MOD_ROLE_ID)
            owner_role = guild.get_role(OWNER_ROLE_ID)

            roles_to_notify = [manager_role, mod_role, owner_role]

            for role in roles_to_notify: 
                if role is not None:
                    # Refresh the member cache to ensure it is up-to-date
                    await guild.chunk()

                    print(f"Role found: {role.name} with {len(role.members)} members")
                    for member in role.members:
                        try:
                            embed = discord.Embed(
                                title=f"New Support Ticket from {message.author}",
                                description=message.content,
                                color=discord.Color.blue()
                            )
                            await member.send(embed=embed)
                            print(f"Sent query to {member}") 
                        except discord.Forbidden:
                            print(f"Could not send DM to {member}")
                        except Exception as e:
                            print(f"An error occurred while sending DM to {member}: {e}")
                else:
                    print(f"Role with ID {role.id} not found.")
        except discord.Forbidden:
            print("Could not send confirmation DM to the user.")
        except Exception as e:
            print(f"An error occurred: {e}")
            print(f"An error occurred: {e}")

 


# Run the bot
bot.run('BOT_TOKEN') #<----------- bot token 

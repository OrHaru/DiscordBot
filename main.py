import os
import discord

client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$hello'):
    await message.channel.send('Hello Bitch')


@client.event
async def on_raw_reaction_add(payload):
  message_id = payload.message_id
  if message_id == 1083126143651168438:
    guild_id = payload.guild_id
    guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
    role = discord.utils.get(guild.roles, name=payload.emoji.name)
    
    if role is not None:
      member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
      if member is not None:
        await member.add_roles(role)
        print("done")
      else:
        print("member not found")
    else:
      print("role not found")

@client.event
async def on_raw_reaction_remove(payload):
  message_id = payload.message_id
  if message_id == 1083126143651168438:
    guild_id = payload.guild_id
    guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
    role = discord.utils.get(guild.roles, name=payload.emoji.name)
    
    if role is not None:
      member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
      if member is not None:
        await member.remove_roles(role)
        print("done")
      else:
        print("member not found")
    else:
      print("role not found")

  

#my_secret = os.environ['TOKEN']
client.run(os.getenv('TOKEN'))

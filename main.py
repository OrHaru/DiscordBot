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
    guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
    role = discord.utils.get(guild.roles, name=payload.emoji.name)

    if role is not None:
      member = discord.utils.find(lambda m: m.id == payload.user_id,
                                  guild.members)
      if member is not None:
        await member.add_roles(role)
        print(
          str(payload.member.name) + "#" + str(payload.member.discriminator) +
          " took the " + str(payload.emoji.name) + " role")
      else:
        print("member not found")
    else:
      print("role not found")


@client.event
async def on_raw_reaction_remove(payload):
  message_id = payload.message_id
  if message_id == 1083126143651168438:
    guild_id = payload.guild_id
    guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
    role = discord.utils.get(guild.roles, name=payload.emoji.name)

    if role is not None:
      member = discord.utils.find(lambda m: m.id == payload.user_id,
                                  guild.members)
      if member is not None:
        print("Removed Role:\n" + str(payload))
        await member.remove_roles(role)

      else:
        print("member not found")
    else:
      print("role not found")


@client.event
async def on_member_join(member):
  embed = discord.Embed(
    title="Welcome to Expensive Brothers server",
    description=
    "To browse and select from various roles, visit the roles channel:\n" +
    "https://discord.com/channels/648219887344418816/944307930960920616/1027311476450537504\n"
    + "Enjoy :)",
    color=0xFF5733)
  await member.send(embed=embed)


#my_secret = os.environ['TOKEN']
client.run(os.getenv('TOKEN'))

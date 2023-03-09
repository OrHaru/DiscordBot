import os
import discord
from keep_alive import keep_alive

client = discord.Client(intents=discord.Intents.all())
invites = {}


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  # Getting all the guilds our bot is in
  for guild in client.guilds:
    # Adding each guild's invites to our dict
    invites[guild.id] = await guild.invites()


@client.event
async def on_invite_create(invite):

  # Adding each guild's invites to our dict
  invites[invite.guild.id] = await invite.guild.invites()


def find_invite_by_code(invite_list, code):

  # Simply looping through each invite in an
  # invite list which we will get using guild.invites()

  for inv in invite_list:

    # Check if the invite code in this element
    # of the list is the one we're looking for

    if inv.code == code:

      # If it is, we return it.

      return inv


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
  embed1 = discord.Embed(
    title="Welcome to Expensive Brothers server",
    description=
    "To browse and select from various roles, visit the roles channel:\n" +
    "https://discord.com/channels/648219887344418816/944307930960920616/1027311476450537504\n"
    + "Enjoy :)",
    color=0xFF5733)
  await member.send(embed=embed1)

  print(member)

  # Getting the invites before the user joining
  # from our cache for this specific guild

  invites_before_join = invites[member.guild.id]

  # Getting the invites after the user joining
  # so we can compare it with the first one, and
  # see which invite uses number increased

  invites_after_join = await member.guild.invites()

  # Loops for each invite we have for the guild
  # the user joined.

  for invite in invites_before_join:

    # Now, we're using the function we created just
    # before to check which invite count is bigger
    # than it was before the user joined.

    if invite.uses < find_invite_by_code(invites_after_join, invite.code).uses:

      # Now that we found which link was used,
      # we will print a couple things in our console:
      # the name, invite code used the the person
      # who created the invite code, or the inviter.

      print(f"Member {member.name} Joined")
      print(f"Invite Code: {invite.code}")
      print(f"Inviter: {invite.inviter}")
      embed2 = discord.Embed(
        title="User joined the server",
        description=member.mention + " " + str(member.joined_at) + " - " +
        str(member.name) + "#" + str(member.discriminator) + "\n" +
        "Invite Code: " + invite.code + " Inviter: " + invite.inviter.mention +
        " - " + str(invite.inviter.name) + "#" +
        str(invite.inviter.discriminator),
        color=0xFF5733)
      channel = member.guild.get_channel(1083167098609614988)
      await channel.send(embed=embed2)

      # We will now update our cache so it's ready
      # for the next user that joins the guild

      invites[member.guild.id] = invites_after_join

      # We return here since we already found which
      # one was used and there is no point in
      # looping when we already got what we wanted
      return


@client.event
async def on_member_remove(member):
  embed2 = discord.Embed(title="User left the server",
                         description=member.mention + " - " +
                         str(member.name) + "#" + str(member.discriminator) +
                         " " + str(member.joined_at),
                         color=0xFF5733)
  channel = member.guild.get_channel(1083167098609614988)
  await channel.send(embed=embed2)


@client.event
async def on_voice_state_update(member, before, after):
  channel = member.guild.get_channel(1083335174504329276)
  if before.channel is None and after.channel is not None:
    embed2 = discord.Embed(title="Channel",
                           description=str(member.name) + " joined " +
                           str(after.channel.name),
                           color=0xFF5733)
    await channel.send(embed=embed2)
  if before.channel is not None and after.channel is None:
    embed2 = discord.Embed(title="Channel",
                           description=str(member.name) + " left " +
                           str(before.channel.name),
                           color=0xFF5733)
    await channel.send(embed=embed2)
  if before.channel is not None and after.channel is not None:
    if before.channel.id != after.channel.id:
      embed2 = discord.Embed(title="Channel",
                             description=str(member.name) + " moved from " +
                             str(before.channel.name) + " to " +
                             str(after.channel.name),
                             color=0xFF5733)
      await channel.send(embed=embed2)


#my_secret = os.environ['TOKEN']
keep_alive()
client.run(os.getenv('TOKEN'))
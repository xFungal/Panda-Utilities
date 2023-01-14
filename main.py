import disnake
from disnake.ext import commands
import os
import random

intents = disnake.Intents.all()
client = commands.Bot(command_prefix=".", case_insensitive=True, intents=intents)
client.remove_command("help")

#Events
@client.event
async def on_ready():
  print('Connected to bot: {}'.format(client.user.name))
  print('Bot ID: {}'.format(client.user.id))
  await client.change_presence(activity=disnake.Game('.help | Bot by EXUS Services'))


#Prefix commands
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: disnake.Member=None, *, banReason=None):
  if user is None:
    embed = disnake.Embed(title="Ban Usage", description="You must provide a user to ban.  A reason is optional.", color=0xA7C7E7)
    await ctx.reply(embed=embed)
    return
  else:
    em = disnake.Embed(title="User Banned", description=f"{user.mention} has been succesfully banned.", color=0xA7C7E7)
    await ctx.reply(embed=em)

    embed = disnake.Embed(title="You Were Banned", description="You have been banned from `Panda's Lounge`.", color=0xA7C7E7)
    embed.add_field(name="Reason", value=banReason, inline=False)
    await user.send(embed=embed)
    await user.ban(reason = banReason)


@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, id: int=None):
  if id is None:
    embed = disnake.Embed(title="Unban Usage", description="You must provide the ID of the user you wish to unban.", color=0xA7C7E7)
    await ctx.reply(embed=embed)
    return

  user = await client.fetch_user(id)
  await ctx.guild.unban(user)

  em = disnake.Embed(title="User Unbanned", description=f"{user} has been succesfully unbanned.", color=0xA7C7E7)
  await ctx.reply(embed=em)
  return


@client.command()
@commands.has_permissions(ban_members=True)
async def kick(ctx, user: disnake.Member=None, *, kickReason=None):
  if user is None:
    embed = disnake.Embed(title="Kick Usage", description="You must provide a user to kick.  A reason is optional.", color=0xA7C7E7)
    await ctx.reply(embed=embed)
    return
  else:
    em = disnake.Embed(title="User Kicked", description=f"{user.mention} has been succesfully kicked.", color=0xA7C7E7)
    await ctx.reply(embed=em)

    embed = disnake.Embed(title="You Were Kicked", description="You have been kicked from `Panda's Lounge`.", color=0xA7C7E7)
    embed.add_field(name="Reason", value=kickReason, inline=False)
    await user.send(embed=embed)
    await user.kick(reason = kickReason)


@client.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: disnake.Member=None, *, reason=None):
  if member is None:
    embed = disnake.Embed(title="Mute Usage", description="You must provide a user to mute.  A reason is optional.", color=0xA7C7E7)
    await ctx.reply(embed=embed)
    return
  guild = ctx.guild
  mutedRole = disnake.utils.get(guild.roles, name="MUTED")

  if not mutedRole:
    mutedRole = await guild.create_role(name="MUTED")

    for channel in guild.channels:
      await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True, add_reactions=False)

  await member.add_roles(mutedRole, reason=reason)

  embed = disnake.Embed(title="Member Muted", description=f"I muted {member.mention} for: **`{reason}`.**", color=0xA7C7E7)
  await ctx.reply(embed=embed)


@client.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: disnake.Member=None):
  if member is None:
    embed = disnake.Embed(title="Unmute Usage", description="You must provide a user to unmute.", color=0xA7C7E7)
    await ctx.reply(embed=embed)
    return
  mutedRole = disnake.utils.get(ctx.guild.roles, name="MUTED")
  await member.remove_roles(mutedRole)

  embed = disnake.Embed(title="Member Unmuted", description=f"I unmuted {member.mention}.", color=0xA7C7E7)
  await ctx.reply(embed=embed)


@client.command()
@commands.has_permissions(ban_members=True)
async def softban(ctx, user: disnake.Member=None, *, reason=None):
  id = user.id
  if user is None:
    embed = disnake.Embed(title="Softban Usage", description="You must provide a user to soft-ban.  A reason is optional.", color=0xA7C7E7)
    await ctx.reply(embed=embed)
    return
  else:
    em = disnake.Embed(title="User Softbanned", description=f"{user.mention} has been succesfully soft-banned.", color=0xA7C7E7)
    await ctx.reply(embed=em)

    embed = disnake.Embed(title="You Were Banned", description="You have been soft-banned from `Panda's Lounge`.", color=0xA7C7E7)
    embed.add_field(name="Reason", value=reason, inline=False)
    await user.send(embed=embed)
    await user.ban(reason = reason)
    await ctx.guild.unban(id)


@client.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel: disnake.TextChannel=None):  
  if channel is None:
    channel = ctx.message.channel
  await channel.set_permissions(ctx.guild.default_role, reason=f"**`{ctx.author}` locked `{channel.name}`.**", send_messages=False)

  embed = disnake.Embed(title="Channel Locked.", description=f"I locked {channel.mention}", color=0xA7C7E7)
  await ctx.reply(embed=embed)


@client.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx, channel: disnake.TextChannel=None):  
  if channel is None:
    channel = ctx.message.channel
  await channel.set_permissions(ctx.guild.default_role, reason=f"**`{ctx.author}` unlocked `{channel.name}`.**", send_messages=True)

  embed = disnake.Embed(title="Channel Unlocked.", description=f"I unlocked {channel.mention}", color=0xA7C7E7)
  await ctx.reply(embed=embed)

@client.command(aliases=['clear', 'clearmessages'])
@commands.has_permissions(ban_members=True)
async def purge(ctx, amount: int=None):
  if amount is None:
    amount = 1

  await ctx.channel.purge(limit=amount)

  embed = disnake.Embed(title="Purge Successful", description=f"Successfully deleted `{amount}` messages!", color=0xA7C7E7)
  await ctx.send(embed=embed, delete_after=5)


@client.command()
async def help(ctx):
  embed = disnake.Embed(title="Help Page", description="You can find all of the commands below.", color=0xA7C7E7)
  embed.add_field(name="Commands", value=
  """
    `help` - Shows this help page.
    `ban` - Ban user from the server.
    `unban` - Allows a banned user to join the server.
    `softban` - Kicks user and removes all their messages.
    `kick` - Kick a user from the server.
    `mute` - Prevent a user from speaking.
    `unmute` - Allow a user to speak.
    `lock` - Lock the specificed or current channel.
    `unlock` - Unlock the specified or current channel.
    `purge` - Remove the specificed number of messages.
  """, inline=False)
  await ctx.reply(embed=embed)



#Slash commands
@client.slash_command(name="help", description="Shows the entire list of all commands.")
async def _help(ctx: disnake.ApplicationCommandInteraction):
  embed = disnake.Embed(title="Help Page", description="You can find all of the commands below.", color=0xA7C7E7)
  embed.add_field(name="Commands", value=
  """
    `help` - Shows this help page.
    `ban` - Ban user from the server.
    `unban` - Allows a banned user to join the server.
    `softban` - Kicks user and removes all their messages.
    `kick` - Kick a user from the server.
    `mute` - Prevent a user from speaking.
    `unmute` - Allow a user to speak.
    `lock` - Lock the specificed or current channel.
    `unlock` - Unlock the specified or current channel.
    `purge` - Remove the specificed number of messages.
  """, inline=False)
  await ctx.response.send_message(embed=embed)



@client.slash_command(name="ban", description="Ban a user from the server.")
async def _ban(ctx: disnake.ApplicationCommandInteraction, user: disnake.Member=None, reason=None):
  if not ctx.author.guild_permissions.ban_members:
    return
  if user is None:
    embed = disnake.Embed(title="Ban Usage", description="You must provide a user to ban.  A reason is optional.", color=0xA7C7E7)
    await ctx.send(embed=embed)
    return
  else:
    em = disnake.Embed(title="User Banned", description=f"{user.mention} has been succesfully banned.", color=0xA7C7E7)
    await ctx.send(embed=em)

    embed = disnake.Embed(title="You Were Banned", description="You have been banned from `Panda's Lounge`.", color=0xA7C7E7)
    embed.add_field(name="Reason", value=reason, inline=False)
    await user.send(embed=embed)
    await user.ban(reason = reason)


@client.slash_command(name="unban", description="Unban a user that is already banned. [Using ID]")
async def _unban(ctx: disnake.ApplicationCommandInteraction, id):
  if not ctx.author.guild_permissions.ban_members:
    return

  user = await client.fetch_user(id)
  await ctx.guild.unban(user)

  em = disnake.Embed(title="User Unbanned", description=f"{user} has been succesfully unbanned.", color=0xA7C7E7)
  await ctx.send(embed=em)
  return


@client.slash_command(name="kick", description="Kicks a user from the server without banning them.")
async def _kick(ctx: disnake.ApplicationCommandInteraction, user, reason):
  if not ctx.author.guild_permissions.kick_members:
    return
  em = disnake.Embed(title="User Kicked", description=f"{user.mention} has been succesfully kicked.", color=0xA7C7E7)
  await ctx.send(embed=em)

  embed = disnake.Embed(title="You Were Kicked", description="You have been kicked from `Panda's Lounge`.", color=0xA7C7E7)
  embed.add_field(name="Reason", value=reason, inline=False)
  await user.send(embed=embed)
  await user.kick(reason = reason)

@client.slash_command(name="mute", description="Prevent the specified user from speaking.")
async def _mute(ctx: disnake.ApplicationCommandInteraction, member: disnake.Member, reason):
  if not ctx.author.guild_permissions.manage_messages:
    return
  guild = ctx.guild
  mutedRole = disnake.utils.get(guild.roles, name="MUTED")

  if not mutedRole:
    mutedRole = await guild.create_role(name="MUTED")

    for channel in guild.channels:
      await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)

  await member.add_roles(mutedRole, reason=reason)

  embed = disnake.Embed(title="Member Muted", description=f"I muted {member.mention} for: **`{reason}`.**", color=0xA7C7E7)
  await ctx.send(embed=embed)

@client.slash_command(name="unmute", description="Allow a user that was already muted to speak again.")
async def _unmute(ctx: disnake.ApplicationCommandInteraction, member: disnake.Member):
  if not ctx.author.guild_permissions.manage_messages:
    return
  mutedRole = disnake.utils.get(ctx.guild.roles, name="MUTED")
  await member.remove_roles(mutedRole)

  embed = disnake.Embed(title="Member Unmuted", description=f"I unmuted {member.mention}.", color=0xA7C7E7)
  await ctx.send(embed=embed)


@client.slash_command(name="lock", description="Prevents everybody from speaking in channel if not a staff.")
async def _lock(ctx: disnake.ApplicationCommandInteraction, channel: disnake.TextChannel):
  if not ctx.author.guild_permissions.manage_channels:
    return
  await channel.set_permissions(ctx.guild.default_role, reason=f"**`{ctx.author}` locked `{channel.name}`.**", send_messages=False)

  embed = disnake.Embed(title="Channel Locked", description=f"I locked {channel.mention}", color=0xA7C7E7)
  await ctx.send(embed=embed)


@client.slash_command(name="unlock", description="Unlocks a channel that was previously locked by a staff member.")
async def _unlock(ctx: disnake.ApplicationCommandInteraction, channel: disnake.TextChannel):
  if not ctx.author.guild_permissions.manage_channels:
    return
  await channel.set_permissions(ctx.guild.default_role, reason=f"**`{ctx.author}` unlocked `{channel.name}`.**", send_messages=True)

  embed = disnake.Embed(title="Channel Unlocked.", description=f"I unlocked {channel.mention}", color=0xA7C7E7)
  await ctx.send(embed=embed)


@client.slash_command(name="purge", description="Removes the specified amount of messages from the current channel.")
async def _purge(ctx: disnake.ApplicationCommandInteraction, amount):
  if not ctx.author.guild_permissions.manage_messages:
    return

  await ctx.channel.purge(limit=int(amount)+1)

  embed = disnake.Embed(title="Purge Successful", description=f"Successfully deleted `{amount}` messages!", color=0xA7C7E7)
  await ctx.send(embed=embed, delete_after=5)



client.run('token here')

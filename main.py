import discord
from discord.ext import commands


intents = discord.Intents.all()
bot = commands.Bot(command_prefix="&", intents=intents)

bot.remove_command("help")

vouches = {}
vouch_messages = {}
vouch_target = None 
vouch_channel = None

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name="setuser")
@commands.has_permissions(administrator=True) 
async def set_user(ctx, member: discord.Member):
    global vouch_target
    vouch_target = member.id
    embed = discord.Embed(
        title="User Set for Vouches",
        description=f"**{member.mention} is now the only user who can receive vouches.**",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

@bot.command(name="set-vouch")
@commands.has_permissions(administrator=True)
async def vouch_channel(ctx, channel: discord.TextChannel):
    global vouch_channel
    vouch_channel = channel.id
    embed = discord.Embed(title="Vouch Channel Set", description=f"{channel.mention} is now the channel for vouches!", color=discord.Color.green())
    await ctx.send(embed=embed)


@bot.command(name="vouch")
async def give_vouch(ctx, target, *, message: str):
    global vouch_target
    target = vouch_target
    if target is None:
        await ctx.send("**User has been set for vouches yet!**")
        return

    elif target == ctx.author.id:
        await ctx.send("**You cannot Vouch for yourself!**")
        return
    target_user = ctx.guild.get_member(target)
    if target_user is None:
        await ctx.send("**The user set for vouches is not in the server!**")
        return

    if target_user.id not in vouches:
        vouches[target_user.id] = 0
        vouch_messages[target_user.id] = []

    vouches[target_user.id] += 1
    if message:
        vouch_messages[target_user.id].append(f"{ctx.author.mention} : {message}")

    elif ctx.channel.id != vouch_channel:
        return 

    else:
        vouch_messages[target_user.id].append(f"{ctx.author.mention}: **No message provided**")

    embed = discord.Embed(
        title="Vouch Added",
        description=f"{ctx.author.mention} has vouched for {target_user.mention}!",
        color=discord.Color.blue()
    )
    if message:
        embed.add_field(name="Vouched Message", value=message, inline=False)

    await ctx.send(embed=embed)

@bot.command(name="profile")
async def profile(ctx, target):
    global vouch_target
    target = vouch_target
    if target is None:
        await ctx.send("**User has been set for vouches yet!**")
    target_user = ctx.guild.get_member(target)
    if target_user is None:
        await ctx.send("**The user set for vouches is not in the server!**")
        return

    vouch_count = vouches.get(target_user.id, 0)
    messages = vouch_messages.get(target_user.id, [])

    embed = discord.Embed(
        title=f"{target_user.name}'s Profile",
        description=f"Total Vouches: {vouch_count}",
        color=discord.Color.purple()
    )

    if messages:
        for msg in messages:
            embed.add_field(name="Vouch Messages", value=msg, inline=False)

    else:
        embed.add_field(name="Vouch Messages", value="No vouch messages yet", inline=False)

    await ctx.send(embed=embed)
    



@bot.command(name="help")
async def help_command(ctx):
    embed = discord.Embed(
        title="Help - Zone Vouches Commands",
        description="Here are the commands you can use:",
        color=discord.Color.orange()
    )
    embed.add_field(name="&setuser <@member>", value="Set the user who can receive vouches (Admin only).", inline=False)
    embed.add_field(name="&vouch  <@user> <message>", value="Vouch for the user", inline=False)
    embed.add_field(name="&profile", value="Check the profile of the user.", inline=False)
    embed.add_field(name="&set-vouch <channel_id>", value="Set the channel for Vouches (admin only)")
    await ctx.send(embed=embed)
    

bot_token = "Token"
bot.run(bot_token)
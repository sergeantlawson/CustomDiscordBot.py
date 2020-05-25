import discord
from discord.ext import commands
from discord.utils import get
import asyncio


bot = commands.Bot(command_prefix="?")
bot.remove_command("help")


@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name + "\n")
    game = discord.Game("")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Spotify"))


@bot.event
async def on_member_join(member):
    guild = member.guild
    s_channel = guild.system_channel
    role = discord.utils.get(member.guild.roles, id=712739971035037776)
    await member.add_roles(role)
    to_send = 'Welcome {0.mention} to {1.name}!'.format(member, guild)
    await s_channel.send(to_send)



@bot.command()
async def request(ctx):
    auth = ctx.author
    au = str(auth)
    role = discord.utils.get(ctx.guild.roles, id=712739882128244736)
    await ctx.message.delete()
    
    if role in auth.roles:
        await ctx.author.send("You have already requested please be patient!")
    else:
        await auth.add_roles(role)
        print(au + "has requested!")
        await ctx.author.send("Thank you for the request an Admin or Moderator shall be in touch with you soon!")
        file = open("requested.txt", "a")
        file.write("\n")
        file.write(au)
        file.close()
        guild = ctx.guild
        reqnoti = discord.utils.get(guild.text_channels, name='request-notifications')
        to_send = '{0.mention} has requested Recovery!'.format(auth)
        await reqnoti.send(to_send)
        
@bot.command()
async def rmrequest(ctx):
    auth = ctx.author
    au = str(auth)
    role = discord.utils.get(ctx.guild.roles, id=712739882128244736)
    await ctx.message.delete()

    if role in auth.roles:
        await auth.remove_roles(role)
        await ctx.author.send("You have been removed from the request queue!")
        f = open('requested.txt','r')
        a = str(auth)
        lst = []
        for line in f:
            for word in a:
                if word in line:
                    line = line.replace(word,'')
            lst.append(line)
        f.close()
        f = open('requested.txt','w')
        for line in lst:
            f.write(line)
        f.close()
    else:
        await ctx.author.send("You have not previously requested, cannot remove!")

print("Loading Token...")
config = open("config.txt")
TOKEN = config.read()
config.close()
bot.run(TOKEN)

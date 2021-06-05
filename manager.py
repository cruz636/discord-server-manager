from discord.ext import commands
import os
import discord
from dotenv import load_dotenv, set_key

class Assistant(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel:discord.VoiceChannel):
        """ Join Voice Channel """
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def stop(self, ctx):
        """ Disconnect bot from voice channel """
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("See you")
        else:
            await ctx.send("I am not connected to a voice channel")

    @commands.command()
    async def edit_welcome_message(self, ctx, message):
        # add the message to the .env
        set_key('.env', 'WELCOME_MESSAGE', message)
        await ctx.send("Welcome message edited :)")

    @commands.command()
    async def welcome_message(self, ctx):
        # see current welcome message
        welcome_message = os.getenv("WELCOME_MESSAGE")
        await ctx.send(welcome_message)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild

        message = "Hey hey hey"
        if guild.system_channel is not None:
            to_send = '{0.mention}! {1}'.format(member, message)
            await guild.system_channel.send(to_send)

    @commands.command()
    async def create_channel(self, ctx, *args):
        name = args[0]

        # default is to create voice and text channels 
        text_channel = True
        voice_channel = True

        # check if the user add options on the call
        if len(args) == 2:
            if args[1] == '-ot':
                voice_channel = False
            if args[1] == '-ov':
                text_channel = False
            else:
                # wrong command wont create any channel
                voice_channel = False
                text_channel = False
                await ctx.send("Wrong command, !help for help ( lol )")
                return

        text_channel_name = name + " text"
        guild = ctx.guild
        
        existing_voice_channel = discord.utils.get(guild.channels, name=name) if voice_channel else False
        
        existing_text_channel = discord.utils.get(guild.channels, name=text_channel_name) if text_channel else False

    
        if voice_channel:
            if not existing_voice_channel:
                await ctx.send("Creating new voice channel")
                await guild.create_voice_channel(name)
            else:
                await ctx.send("The name is already in use")

        if text_channel:
            if not existing_text_channel:
                await ctx.send("Creating text channel")
                await guild.create_text_channel(text_channel_name)
            else:
                await ctx.send("The name is already in use")

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), )

@bot.event
async def on_ready():
    print("Logged in as {} \n".format(bot.user))

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot.add_cog(Assistant(bot))
bot.run(TOKEN)

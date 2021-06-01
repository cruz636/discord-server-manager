from discord.ext import commands
import os
import discord
from dotenv import load_dotenv

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
    async def create_channel(self, ctx, *args):
        name = args[0]
        text_channel = True if len(args) == 1  else False
        text_channel_name = name + " text"
        guild = ctx.guild
        
        existing_channel = discord.utils.get(guild.channels, name=name) or discord.utils.get(guild.channels, name=text_channel_name)

        if not existing_channel:
            await ctx.send("Creating new voice channel")
            await guild.create_voice_channel(name)

            if text_channel:
                await ctx.send("Creating text channel")
                await guild.create_text_channel(text_channel_name)
        else:
            await ctx.send("The name is already being used for other channel")

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), )

@bot.event
async def on_ready():
    print("Logged in as {} \n".format(bot.user))

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot.add_cog(Assistant(bot))
bot.run(TOKEN)

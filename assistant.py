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
        """ Disconnect bot from channel """
        await ctx.voice_client.disconnect()

    @commands.command()
    async def create_channel(self, ctx, *, name, text_channel=True):
        channel_name = name
        if text_channel:
            await ctx.send("Creating text channel")
        ctx.send("Creating voice channel")

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!AB"), )

@bot.event
async def on_ready():
    print("Logged in as {} \n".format(bot.user))

load_doatenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot.add_cog(Assistant(bot))
bot.run(TOKEN)

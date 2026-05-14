import discord
from discord.ext import commands
import config

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'✅ PyWumpus connecté en tant que {bot.user}')
    await bot.load_extension('cogs.builds')
    await bot.load_extension('cogs.experiments')
    print('✅ Tous les Cogs chargés !')

if __name__ == "__main__":
    bot.run(config.TOKEN)

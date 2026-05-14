import discord
from discord.ext import commands, tasks
import json
import os
from utils.scraper import fetch_experiments
from config import EXP_CHANNEL

class Experiments(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.previous_exps = self.load_previous()
        self.check_experiments.start()

    def load_previous(self):
        os.makedirs('data', exist_ok=True)
        if os.path.exists('data/last_experiments.json'):
            try:
                with open('data/last_experiments.json') as f:
                    return json.load(f)
            except:
                return []
        return []

    @tasks.loop(minutes=10)
    async def check_experiments(self):
        current = await fetch_experiments()
        # Simple detection of new ones (by length or hash for demo)
        if len(current) > len(self.previous_exps) + 5:  # Threshold to avoid noise
            channel = self.bot.get_channel(EXP_CHANNEL)
            if channel:
                embed = discord.Embed(title="🧪 Nouvelles expériences détectées !", color=0xF04747)
                embed.description = f"{len(current) - len(self.previous_exps)} nouvelles expériences possibles"
                await channel.send(embed=embed)
        self.previous_exps = current
        with open('data/last_experiments.json', 'w') as f:
            json.dump(current, f, indent=2)

    @commands.command()
    async def experiments(self, ctx):
        """Affiche le nombre d'expériences actuelles"""
        data = await fetch_experiments()
        await ctx.send(f"📊 {len(data)} expériences/guild experiments détectées actuellement.")

async def setup(bot):
    await bot.add_cog(Experiments(bot))

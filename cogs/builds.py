import discord
from discord.ext import commands, tasks
import json
import os
from utils.scraper import fetch_discord_builds
from config import BUILD_CHANNEL

class Builds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.previous_builds = self.load_previous()
        self.check_builds.start()

    def load_previous(self):
        os.makedirs('data', exist_ok=True)
        if os.path.exists('data/last_builds.json'):
            try:
                with open('data/last_builds.json') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    @tasks.loop(minutes=5)
    async def check_builds(self):
        current = await fetch_discord_builds()
        for branch, info in current.items():
            old = self.previous_builds.get(branch)
            if old and old.get('build_number') != info.get('build_number'):
                channel = self.bot.get_channel(BUILD_CHANNEL)
                if channel:
                    embed = discord.Embed(title=f"🚀 Nouveau build {branch.upper()} !", color=0x5865F2)
                    embed.add_field(name="Version", value=info.get('version', 'N/A'), inline=False)
                    embed.add_field(name="Build", value=info.get('build_number', 'N/A'), inline=True)
                    await channel.send(embed=embed)
        self.previous_builds = current
        with open('data/last_builds.json', 'w') as f:
            json.dump(current, f, indent=2)

    @commands.command()
    @commands.is_owner()
    async def builds(self, ctx):
        data = await fetch_discord_builds()
        embed = discord.Embed(title="Discord Builds Actuels", color=0x5865F2)
        for branch, info in data.items():
            embed.add_field(name=branch.upper(), value=f"**Build:** {info.get('build_number')}\n**Version:** {info.get('version')}", inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Builds(bot))

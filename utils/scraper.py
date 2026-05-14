import aiohttp

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

async def fetch_discord_builds():
    urls = {
        "stable": "https://discord.com/api/updates/stable?platform=win",
        "ptb": "https://discord.com/api/updates/ptb?platform=win",
        "canary": "https://discord.com/api/updates/canary?platform=win"
    }
    async with aiohttp.ClientSession() as session:
        results = {}
        for branch, url in urls.items():
            try:
                async with session.get(url, headers=HEADERS) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        results[branch] = {
                            "build_number": data.get("build_number"),
                            "version": data.get("name"),
                            "hash": data.get("hash")
                        }
            except:
                pass
        return results

async def fetch_experiments():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get("https://discord.com/api/v9/experiments", headers=HEADERS) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("assignments", []) + data.get("guild_experiments", [])
        except:
            pass
    return []
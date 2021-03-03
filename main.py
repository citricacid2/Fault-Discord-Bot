from discord.ext import commands
# ^ basic imports for other features of discord.py and python ^

import requests
import re
import random

types = {
    'jungler': 'JUNGLE',
    'support': 'SUPPORT',
    'carry': 'ADC',
    'midlane': 'MID',
    'offlane': 'OFFLANE'
}

client = commands.Bot(command_prefix='!')  # put your own prefix here


@client.event
async def on_ready():
    print("bot online")  # will print "bot online" in the console when the bot is online


@client.command()
async def pick(ctx, amount=1):
    """Returns random heroes: Usage !pick <amount> """
    site = requests.get('https://api.playfault.com/getStatsPerHero').json()
    message = ""
    for i in range(amount):
        name = random.choice(list(site['heroes'].keys()))
        site['heroes'].pop(name)
        message += name
        message += '\n'
    await ctx.send(message)


@client.command()
async def position(ctx, name):
    """Returns a random type: Usage !position <type>"""
    site = requests.get('https://faultmetrics.com/builds')

    try:
        match = re.findall(
            r'&quot;api_hero_name&quot;:&quot;(\S*?)&quot;,&quot;typical_position&quot;:&quot;{}&quot;'.format(
                types[name]), site.text)
        await ctx.send(random.choice(match))
    except KeyError:
        await ctx.send("Type does not exist. Must be in " + str(list(types.keys())))


@client.command()
async def elo(ctx, username):
    """Returns the ELO of a player: Usage !elo <username>"""
    site = requests.get(f'https://faultmetrics.com/players/{username}')
    if site.status_code == 404:
        await ctx.send('User does not exist')
        return

    match = re.search(r'&quot;elo&quot;:(\d*?),', str(site.content))

    await ctx.send(f"ELO is {match.group(1)}")


@client.command()
async def coinflip(ctx):
    """Heads or Tails: Usage !coinflip"""
    if random.randint(0, 1):
        await ctx.send('Heads!')
    else:
        await ctx.send('Tails!')


@client.command()
async def stats(ctx, username):
    """Returns player stats: Usage !stats <username>"""
    site = requests.get(f'https://faultmetrics.com/players/{username}')
    if site.status_code == 404:
        await ctx.send('User does not exist')
        return

    match = re.search(
        r'&quot;matchCount&quot;:(\d*?),&quot;wins&quot;:(\d*?),&quot;kills&quot;:&quot;(\d*?)&quot;,'
        r'&quot;deaths&quot;:&quot;(\d*?)&quot;,&quot;assists&quot;:&quot;(\d*?)&quot;',
        site.text)

    await ctx.send(f"""
Wins: {match.group(2)}
Win Rate: {int(match.group(2)) / int(match.group(1)) * 100}%
Kills: {match.group(3)}
Deaths: {match.group(4)}
Assists: {match.group(5)}
    """)

token = input("Enter token:")
client.run(token)

import os
import json
import discord
import random
from collections import defaultdict
from dotenv import load_dotenv

client = discord.Client()
load_dotenv()

weapons_file = open('../resources/json/csgo-weapons.json', 'r')
weapons = json.load(weapons_file)
weapons_file.close()


def group_by_group_id(elements):
    groups = defaultdict(list)
    for obj in elements:
        groups[obj['group_id']].append(obj)
    return groups.values()


pistols = list(group_by_group_id(weapons['pistols']))
weapons = list(group_by_group_id(weapons['weapons']))


@client.event
async def on_ready():
    print('Bot is logged as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/crw'):
        random_pistols = get_random_element(pistols)
        random_weapons = get_random_element(weapons)

        response = format_response(random_pistols, random_weapons)

        await message.channel.send(response)


def get_random_element(elements):
    if not elements:
        return
    return random.choice(elements)


def format_response(random_pistols, random_weapons):
    return "Your weapons are : " + "/".join([p['name'] for p in random_pistols]) + " and " + "/".join(
        [w['name'] for w in random_weapons])


client.run(os.getenv('CRWD_BOT_TOKEN'))

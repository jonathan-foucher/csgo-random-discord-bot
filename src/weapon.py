import json
import os
from collections import defaultdict
from io import BytesIO

import discord
from PIL import Image

script_dir = os.path.dirname(__file__)

weapons_file_path = os.path.join(script_dir, '../resources/json/csgo-weapons.json')
weapons_file = open(weapons_file_path, 'r')
weapons_json = json.load(weapons_file)
weapons_file.close()


class Weapon:
    def __init__(self, name, image):
        self.name = name
        self.image = image


def get_weapons_image(weapons_list):
    images = [Image.open(os.path.join(script_dir, '../resources/img/{}.png'.format(weapon['name'].replace(' ', '_'))))
              for weapon in weapons_list]
    width, height = tuple(s // 4 for s in images[0].size)
    images = [i.resize((width, height), Image.ANTIALIAS) for i in images]

    total_width = width * len(images)
    combined_im = Image.new('RGBA', (total_width, height))

    x_offset = 0
    for im in images:
        combined_im.paste(im, (x_offset, 0))
        x_offset += width

    with BytesIO() as image_binary:
        combined_im.save(image_binary, 'PNG')
        image_binary.seek(0)
        return discord.File(fp=image_binary, filename='weapon.png')


def generate_weapons_list(weapons_type):
    groups = defaultdict(list)
    for wpn in weapons_json[weapons_type]:
        groups[wpn['group_id']].append(wpn)

    weapons_list = list()
    for wpn_group in groups.values():
        wpn_name = "/".join([w['name'] for w in wpn_group])
        wpn_image = get_weapons_image(wpn_group)
        weapons_list.append(Weapon(wpn_name, wpn_image))
    return weapons_list

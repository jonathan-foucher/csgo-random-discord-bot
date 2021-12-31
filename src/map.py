import copy
import glob
import os
import re
from io import BytesIO

import discord
from PIL import Image

from utils import get_random_element

script_dir = os.path.dirname(__file__)
maps_folder = os.path.join(script_dir, '..\\resources\\img\\maps\\*.png')
maps_paths = glob.glob(maps_folder)


class Map:
    def __init__(self, name, image):
        self.name = name
        self.image = image


def get_maps_image(map_path):
    image = Image.open(map_path)
    width, height = tuple(s // 4 for s in image.size)
    image = image.resize((width, height), Image.ANTIALIAS)

    with BytesIO() as image_binary:
        image.save(image_binary, 'PNG')
        image_binary.seek(0)
        return discord.File(fp=image_binary, filename='map.png')


def generate_maps_list():
    maps_list = list()
    for map_path in maps_paths:
        map_name = re.search('[^\\\\]*\\.(\\w+)$', map_path).group()[:-4]
        map_image = get_maps_image(map_path)
        maps_list.append(Map(map_name, map_image))
    return maps_list


async def send_random_map(channel):
    random_map = get_random_element(maps)
    response = 'You will be playing on {}'.format(random_map.name)
    await channel.send(response, file=copy.deepcopy(random_map.image))


maps = generate_maps_list()

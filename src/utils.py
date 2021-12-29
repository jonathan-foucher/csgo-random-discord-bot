import random


def get_random_element(elements):
    if not elements:
        return
    return random.choice(elements)

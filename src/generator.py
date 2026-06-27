import random
import json

with open("data/dataset.json", "r") as f:
    data = json.load(f)

greetings = data['greetings']
farewells = data['farewells']

def gen_hello():
    return random.choice(greetings)

def gen_goodbye():
    return random.choice(farewells)
import random
import json
with open("data/dataset.json", "r") as f:
    data = json.load(f)

greetings = data['greetings']

def gen_hello():
    return random.choice(greetings)
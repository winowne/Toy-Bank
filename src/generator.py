import random
import json
from pathlib import Path

with (Path(__file__).resolve().parent.parent / "data" / "dataset.json").open(
    encoding="utf-8"
) as f:
    data = json.load(f)

greetings = data['greetings']
farewells = data['farewells']

def gen_hello():
    return random.choice(greetings)

def gen_goodbye():
    return random.choice(farewells)

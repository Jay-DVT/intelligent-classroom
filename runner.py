import requests
from collections import defaultdict
from db_init import conn
from pdf_handler import extract_from_local

c = conn.cursor()

COMPONENTS_API_ADDRESS = '127.0.0.1:8000/api/'


class Class:
    def __init__(self, setupHashmap, instructions) -> None:
        self.counter = 0
        self.presentation_link = setupHashmap['PRESENTATION']
        self.song_link = setupHashmap['SONG'] if 'SONG' in setupHashmap.keys(
        ) else None
        self.instructions = [instructions[k] for k in instructions]
        try:
            self.presentation_length = self.load_media()
        except:
            print("Error loading presentation")
            exit()

    def load_media(self):
        # change to extract from google drive first
        return extract_from_local(self.presentation_link + '.pdf')

    def next_step(self):
        for k, v in self.instructions[self.counter].items():
            print(k, v)
        self.counter += 1


def search_available_classes():
    data = c.execute(f"SELECT serial, name, id FROM class")
    available = {i: {
        "serial": presentation[0],
        "name": presentation[1],
        "id": presentation[2]
    }
        for i, presentation in enumerate(data.fetchall())
    }
    return available


def create_class(class_id):
    print(f"Running class {class_id}")
    data = c.execute(
        f"SELECT step_number, component, parameter FROM instruction WHERE class_id = {class_id}")
    instructions = data.fetchall()
    instructions = sorted(instructions, key=lambda x: x[0])
    setup = {}
    while instructions and instructions[0][0] == 0:
        _, component, parameter = instructions.pop(0)
        if component not in ['CLASS']:
            setup[component] = parameter
    steps = defaultdict(dict)
    for instruction in instructions:
        step, component, parameter = instruction
        steps[step][component] = parameter

    return Class(setup, steps)


if __name__ == "__main__":
    classes = search_available_classes()
    print("Available classes:")
    print("\tSerial\tName")
    for k, v in classes.items():
        print(f"{k}\t{v['serial']}\t{v['name']}")

    print("Choose a class to work with:")
    while True:
        try:
            choice = int(input())
            if choice not in range(len(classes)):
                raise ValueError
            break
        except ValueError:
            print("Invalid choice. Try again.")
            continue
    create_class(classes[choice]['id'])

import requests
from collections import defaultdict
from db_init import conn

c = conn.cursor()

COMPONENTS_API_ADDRESS = '127.0.0.1:8000/api/'


class Class:
    def __init__(self, setupHashmap, instructions) -> None:
        self.presentation_link = setupHashmap['PRESENTATION']
        self.song_link = setupHashmap['SONG'] if 'SONG' in setupHashmap.keys(
        ) else None
        self.instructions = [instructions[k] for k in instructions]
        print(self.instructions)

    def load_media(self):
        pass

    def start_class(self):
        self.load_media()
        for step in self.instructions:
            for key in step:
                address = COMPONENTS_API_ADDRESS + \
                    key.lower() + '/' + step[key].lower()
                print(address)
            input()


def search_available_classes():
    data = c.execute(f"SELECT serial, name, id FROM class")
    return data.fetchall()


def run_class(class_id):
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

    curr_class = Class(setup, steps)
    curr_class.start_class()


if __name__ == "__main__":
    classes = search_available_classes()
    print("Available classes:")
    print("\tSerial\tName")
    for i, presentation in enumerate(classes):
        serial, name, idx = presentation
        print(f"{i}\t{serial}\t{name}")
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
    run_class(classes[choice][2])

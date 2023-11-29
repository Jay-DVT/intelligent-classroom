import os
import sqlite3
from collections import namedtuple
from app import DATABASE_NAME

os.chdir('./projects')
WORKING_DIRECTORY = os.getcwd()
IMPORTANT_PARAMS = ['PRESENTATION', 'CLASS']
INSTRUCTION_START = 'Step'
files = [f for f in os.listdir() if os.path.isfile(f)]
Instruction = namedtuple("Instruction", "component parameter")


def error(message, l=0):
    print(f"{message} at {l}")
    exit()


def parse_line(line):
    line = line.strip().split(" ")
    if len(line) > 2:
        error("badly formatted line", " ".join(line))
    if len(line) == 1:
        line.append("")
    return line


def get_class_id(serial: str):
    conn = sqlite3.connect(DATABASE_NAME)
    cur = conn.cursor()
    data = cur.execute(f"SELECT id FROM class WHERE serial = '{serial}'")
    result = data.fetchone()
    conn.close()
    if not result:
        error("class not found")
    return result[0]


def save_instruction(class_id: int, step: int, component: str, parameter: str):
    conn = sqlite3.connect(DATABASE_NAME)
    cur = conn.cursor()
    cur.execute(f"""INSERT INTO instruction 
                (step_number, component, parameter, class_id)
                VALUES
                ({step}, '{component}', '{parameter}', {class_id})
                """)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    class_id = 0
    projects = []
    for file in files:
        instructions = []
        with open(f"{WORKING_DIRECTORY}/{file}", "r") as f:
            setup = []
            instructions = [setup]
            # designate the parameters inside the setup
            command, parameter = parse_line(f.readline())
            if command != 'Options':
                error("Options are missing")
            for line in f:
                command, parameter = parse_line(line)
                if command == INSTRUCTION_START:
                    break
                setup.append(Instruction(command, parameter))

            setup_parameters = [x.component for x in setup]
            for param in IMPORTANT_PARAMS:
                if not param in setup_parameters:
                    error(f"{param} is missing in setup")

            for instruction in setup:
                if instruction.component.upper() == 'CLASS':
                    class_id = get_class_id(instruction.parameter)

            step_instructions = []
            for line in f:
                command, parameter = parse_line(line)
                if command == INSTRUCTION_START:
                    instructions.append(step_instructions)
                    step_instructions = []
                else:
                    step_instructions.append(Instruction(command, parameter))

        for idx, step in enumerate(instructions):
            for instruction in step:
                save_instruction(class_id, idx, instruction.component,
                                 instruction.parameter)

import sqlite3
import os
from pdf_handler import extract_from_local
from app import DATABASE_NAME, WORKING_PATH


def search_available_classes():
    os.chdir(WORKING_PATH)
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    data = c.execute(f"SELECT serial, name, id FROM class")
    available = {i: {
        "serial": presentation[0],
        "name": presentation[1],
        "id": presentation[2]
    }
        for i, presentation in enumerate(data.fetchall())
    }

    conn.close()

    return available


def setup_class(class_id):
    print(WORKING_PATH)
    os.chdir(WORKING_PATH)
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    data = c.execute(
        f"SELECT component, parameter FROM instruction WHERE step_number = 0 AND class_id = {class_id}")
    setup = data.fetchall()
    conn.close()
    information = {}
    for instruction in setup:
        component, parameter = instruction
        component = component.upper()
        match component:
            case 'PRESENTATION':
                information['total_slides'] = extract_from_local(
                    download_from_drive(parameter))
            case _:
                continue

    return information


def download_from_drive(address):
    # implement google connection
    return address + '.pdf'


def run_instructions(class_id, step):
    os.chdir(WORKING_PATH)
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    data = c.execute(
        f"SELECT component, parameter FROM instruction WHERE step_number = {step} AND class_id = {class_id}")
    step = data.fetchall()
    print(step)

    conn.close()

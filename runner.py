import sqlite3
import os
import time
import requests
from dotenv import load_dotenv
from pdf_handler import extract_from_local
from app import DATABASE_NAME, WORKING_PATH

load_dotenv()

COMPONENTS_API_ADDRESS = os.environ.get('COMPONENTS_API_ADDRESS')


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
    os.chdir(WORKING_PATH)
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    data = c.execute(
        f"SELECT MAX(step_number) FROM instruction WHERE class_id = {class_id}"
    )
    information = {}
    information['total_steps'] = data.fetchone()[0]

    data = c.execute(
        f"SELECT component, parameter FROM instruction WHERE step_number = 0 AND class_id = {class_id}")
    setup = data.fetchall()
    conn.close()
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
    conn.close()
    parameters = {}
    for component, parameter in step:
        component = component.capitalize()
        parameter = parameter.lower()
        match component:
            case 'Screen':
                parameters[component] = parameter
            case 'Sound':
                parameters[component] = parameter
            case 'Delay':
                parameters[component] = parameter
            case _:
                address = f"http://{COMPONENTS_API_ADDRESS}?component={component.lower()}&instruction={parameter.lower()}"
                print(address)
                try:
                    # response = requests.put(address)
                    # print(response)
                    time.sleep(1)
                except:
                    print("Error")
                    continue
    return parameters

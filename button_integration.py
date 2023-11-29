import RPi.GPIO as GPIO
import websocket
import json
import threading
import time

# GPIO setup
button_pin = 17  # Replace with your actual GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def on_button_press(ws):
    while True:
        input_state = GPIO.input(button_pin)
        if input_state == False:
            print('Button Pressed')
            ws.send(json.dumps({'action': 'next'}))
            # Debounce
            time.sleep(0.3)


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    print("WebSocket connected")
    # Start a thread to listen for button presses
    threading.Thread(target=on_button_press, args=(ws,)).start()


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://your_flask_server_address",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()

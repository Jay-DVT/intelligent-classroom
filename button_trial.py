import websocket
import json
import threading


def on_key_press(ws):
    while True:
        input("Press Enter to go to the next slide...")
        print('Next slide triggered')
        ws.send(json.dumps({'action': 'next'}))


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    print("WebSocket connected")
    # Start a thread to listen for keyboard input
    threading.Thread(target=on_key_press, args=(ws,)).start()


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://your_flask_server_address",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()

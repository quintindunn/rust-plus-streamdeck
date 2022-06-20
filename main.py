import threading
import time

import websocket
import sys
import json
import rel
from images import off, on

import asyncio
from rustplus import RustSocket

args = sys.argv[1:]
port = args[1]
uuid = args[3]
registerEvent = args[5]
info = args[7]

rs = None
ready = False
loop = asyncio.new_event_loop()

settings = {}

buttons = {
}


def update():

    new_loop = asyncio.new_event_loop()
    while True:
        for button in buttons:
            eid = buttons[button]['eid']
            if eid:
                state = new_loop.run_until_complete(get_state(eid))
                if state != buttons[button]['state']:
                    set_display(state, ctx=buttons[button]['context'])
                    buttons[button]['state'] = state
                time.sleep(0.5)
            if not ready or not rs or not rs.heartbeat.running or not eid:
                socket.send(json.dumps({
                    "event": "showAlert",
                    "context": buttons[button]['context'],
                }))
        time.sleep(1)


threading.Thread(target=update, daemon=True).start()


def set_text(msg, ctx):
    socket.send(json.dumps(
        {
            "event": "setTitle",
            "context": ctx,
            "payload": {
                "title": f"{msg}",
                "target": '0',
            }
        }
    ))


def set_image(image, ctx):
    socket.send(json.dumps(
        {
            "event": "setImage",
            "context": ctx,
            "payload": {
                "image": image,
                "target": '0',
            }
        }
    ))


def set_display(state, ctx):
    set_text('ON' if state else "OFF", ctx)
    set_image(on if state else off, ctx)


def send_to_plugin(ws: websocket.WebSocket, msg):
    key, value = list(msg['payload'].keys())[0], list(msg['payload'].values())[0]
    print(key, value)
    set_setting(ws, msg['context'], key, value)
    ws.send(json.dumps({
        "event": "getSettings",
        "context": msg['context']
    }))


def set_setting(ws: websocket.WebSocket, ctx, key, value):
    global settings

    if key == "eid" and value:
        if value == "RESET":
            settings = {}
        for button in buttons:
            if buttons[button]['context'] == ctx:
                buttons[button]['eid'] = int(value)

    settings[key] = value if value else None
    data = {
        "event": "setSettings",
        "context": ctx,
        "payload": settings
    }
    ws.send(json.dumps(data))


def receive_settings(ws: websocket.WebSocket, msg):
    global settings
    global rs
    global ready
    context = msg['context']
    settings = msg['payload']['settings']
    if settings['eid']:
        for button in buttons:
            if buttons[button]['context'] == context:
                buttons[button]['eid'] = int(settings['eid'])

    if not ready and all([(i in settings and bool(settings[i])) for i in ["Port", "ServerIP", "playerToken", "s64"]]):
        print(settings)
        rs = RustSocket(ip=settings['ServerIP'],
                        port=settings['Port'],
                        player_token=int(settings['playerToken']),
                        steam_id=int(settings['s64']))
        time.sleep(1)
        loop.run_until_complete(rs.connect())
        ready = True
    print(settings)


async def toggle(eid: int, ctx, btn):
    state = await get_state(eid)
    if state:
        await rs.turn_off_smart_switch(eid)
    else:
        await rs.turn_on_smart_switch(eid)

    set_display(state, ctx=ctx)
    buttons[btn]['state'] = state


async def get_state(eid: int):
    if rs and ready:
        data = await rs.get_entity_info(eid)
        return data.value
    return False


def on_message(ws: websocket.WebSocket, message):
    msg = json.loads(message)
    event = msg['event']
    match event:
        case "keyDown":
            on_key_down(ws=ws, msg=msg)

        case "keyUp":
            on_key_up(ws=ws, msg=msg)

        case "willAppear":
            will_appear(ws=ws, msg=msg)

        case "sendToPlugin":
            send_to_plugin(ws=ws, msg=msg)

        case "didReceiveSettings":
            receive_settings(ws=ws, msg=msg)

        case _:
            print(msg)


def on_error(ws: websocket.WebSocket, error):
    print(error)


def on_close(ws: websocket.WebSocket, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws: websocket.WebSocket):
    data = {
        "event": registerEvent,
        "uuid": uuid
    }
    ws.send(json.dumps(data))

    print("Opened connection")


def on_key_down(ws: websocket.WebSocket, msg):
    x, y = msg['payload']['coordinates'].values()
    ctx = msg['context']
    if buttons[f"{x},{y}"]['eid']:
        loop.run_until_complete(toggle(buttons[f"{x},{y}"]['eid'], ctx, f"{x},{y}"))


def on_key_up(ws: websocket.WebSocket, msg):
    print("key_up", msg)


def will_appear(ws: websocket.WebSocket, msg):
    x, y = msg['payload']['coordinates'].values()
    buttons[f"{x},{y}"] = {
        "context": msg['context'],
        "eid": None,
        "state": False
    }

    ws.send(json.dumps({
        "event": "getSettings",
        "context": msg['context']
    }))

    set_display(buttons[f"{x},{y}"]['state'], buttons[f"{x},{y}"]['context'])



if __name__ == "__main__":
    socket = websocket.WebSocketApp(f"ws://127.0.0.1:{port}",
                                    on_open=on_open,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)

    socket.run_forever(dispatcher=rel)
    rel.signal(2, rel.abort)
    rel.dispatch()

import asyncio
import socketio_v4 as socketio
import gpiod
import time
from gpiod.line import Direction, Value

sio = socketio.AsyncClient()

value = Value.INACTIVE
request = []

BUTTON_PUSH    = Value.ACTIVE
BUTTON_RELEASE = Value.INACTIVE


BTN_BET   = 17
BTN_SPIN  = 24
BTN_STOP1 = 23
BTN_STOP2 = 22
BTN_STOP3 = 18

def btn_push(id, wait_time = 0.15):
    print("btn_push %d"%(id))
    request.set_value(id,BUTTON_PUSH);
    time.sleep(wait_time);
    request.set_value(id,BUTTON_RELEASE);

@sio.event
async def connect():
    print('connection established')
    await sio.emit('join-room', {'machine_id': 1}, namespace='/slot')

@sio.event
async def disconnect(sid):
    print('disconnected from server ', sid)

@sio.on('event', namespace='/slot')
async def on_event(data):
    print('event ', data)
    if(data["event"] == "bet"):
        print("Got Bet")
        btn_push(BTN_BET)
    if(data["event"] == "spin"):
        print("Got Spin")
        btn_push(BTN_SPIN)
    if(data["event"] == "stopSpin"):
        print("Got StopSpin %s"% data["data"]["button"])
        if(data["data"]["button"] == "1"):
            btn_push(BTN_STOP1)
        elif (data["data"]["button"] == "2"):
            btn_push(BTN_STOP2)
        elif (data["data"]["button"] == "3"):
            btn_push(BTN_STOP3)
        else:
            print("No Support")


@sio.on('broadcast', namespace='/slot')
async def on_broadcast(data):
    print('broadcast ', data)

async def main():
    await sio.connect('wss://php-slot-api-ws.hmtech-dev.com', transports=['websocket'])
    # await sio.connect('ws://0.0.0.0:9502', transports=['websocket'])
    await sio.wait()

if __name__ == '__main__':
    value_str = {Value.ACTIVE: "Active", Value.INACTIVE: "Inactive"}

    request = gpiod.request_lines(
        "/dev/gpiochip4",
        consumer="toggle-line-value",
        config={
            BTN_BET: gpiod.LineSettings(
                direction=Direction.OUTPUT, output_value=value
            ),
            BTN_SPIN: gpiod.LineSettings(
                direction=Direction.OUTPUT, output_value=value
            ),
            BTN_STOP1: gpiod.LineSettings(
                direction=Direction.OUTPUT, output_value=value
            ),
            BTN_STOP2: gpiod.LineSettings(
                direction=Direction.OUTPUT, output_value=value
            ),
            BTN_STOP3: gpiod.LineSettings(
                direction=Direction.OUTPUT, output_value=value
            ),
        },
    )

    while(1):
        btn_push(BTN_BET)
        sleep(0.75)
        btn_push(BTN_SPIN)
        sleep(0.75)
        btn_push(BTN_STOP1)
        sleep(0.75)
        btn_push(BTN_STOP2)
        sleep(0.75)
        btn_push(BTN_STOP3)
        sleep(0.75)

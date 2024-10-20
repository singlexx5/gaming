import asyncio

import socketio_v4 as socketio

sio = socketio.AsyncClient()

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

@sio.on('broadcast', namespace='/slot')
async def on_broadcast(data):
    print('broadcast ', data)

async def main():
    await sio.connect('wss://php-slot-api-ws.hmtech-dev.com', transports=['websocket'])
    # await sio.connect('ws://0.0.0.0:9502', transports=['websocket'])
    await sio.wait()

if __name__ == '__main__':
    asyncio.run(main())

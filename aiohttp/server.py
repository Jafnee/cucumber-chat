import json
import logging
from uuid import uuid4
import time

import aiohttp
from aiohttp import web
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

routes = web.RouteTableDef()

websockets = {}

while True:
    try:
        producer = KafkaProducer(bootstrap_servers='kafka:9092')
        break
    except NoBrokersAvailable:
        print("Kafka no available :/")
        time.sleep(3)

@routes.get('/')
async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    uid = str(uuid4())
    websockets[uid] = ws
    logger.debug("%s has connected", uid)

    async for msg in ws:
        logger.debug('%s new message', msg)
        if msg.type == aiohttp.WSMsgType.TEXT:
            try:
                data = json.loads(msg.data)
            except json.JSONDecodeError:
                continue
            for socket in websockets.values():
                await socket.send_json(data)
            producer.send('message', msg.data.encode('utf8'))

    del websockets[uid]
    print('websocket connection closed')
    logger.debug("%s has disconnected", uid)
    return ws


app = web.Application()
app.add_routes(routes)
web.run_app(app)

import asyncio
import json

from cassandra.cluster import Cluster, NoHostAvailable
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable


async def main():
    while True:
        try:
            cluster = Cluster(['cassandra'])
            break
        # TODO elegantify all dis sheet.
        except NoHostAvailable:
            print(':( where ya at cass')
            await asyncio.sleep(5)
    while True:
        try:
            consumer = KafkaConsumer('message', bootstrap_servers='kafka:9092')
            break
        except NoBrokersAvailable:
            # TODO elegantify all dis sheet.
            print(':( kafka where u at')
            await asyncio.sleep(5)
    session = cluster.connect('cucumber_chat')
    for msg in consumer:
        print(msg.value)
        data = json.loads(msg.value.decode('utf8'))
        session.execute(
            """
            INSERT INTO messages (id, username, message)
            VALUES (now(), %s, %s)
            """,
            (data['username'], data['message'])
        )

if __name__ == "__main__":
    asyncio.run(main())

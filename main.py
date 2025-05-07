import asyncio
import logging
import signal
import sys

from gql import Client, gql
from gql.transport.websockets import WebsocketsTransport

def signal_handler(signum, frame):
    sys.exit()

async def subscribe_readings():
    transport = WebsocketsTransport(
        url="wss://provider-api.stage.iometer.cloud/v1/query",
        init_payload={
            'authorization': 'Basic YOUR_TOKEN_HERE',
        },
        ping_interval=60,
        pong_timeout=10,
    )

    try:
        async with Client(
                transport=transport,
                fetch_schema_from_transport=True,
        ) as session:
            subscription = gql(
                """
                   subscription {
                        readings {
                        receiveTime,
                        time,
                        meter {
                            number
                        }
                        values {
                            obisCode,
                            value
                            unit
                        }
                    }
                }
            """
            )
            try:
                async for result in session.subscribe(subscription):
                    print(result)
            except Exception as e:
                logging.error(e)
    except Exception as e:
        logging.error(e)


logging.basicConfig(level=logging.ERROR)
signal.signal(signal.SIGINT, signal_handler)
asyncio.run(subscribe_readings())

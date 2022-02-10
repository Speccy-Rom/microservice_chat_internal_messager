import aiormq
import json
from termcolor import cprint
from settings import UNIQUE_PREFIX
from settings import AMQP_URI


async def send_message_to_external_main(outcoming_message_dict):
    cprint(f"AMQP PRODUCER:     send_message_to_external_main {outcoming_message_dict}", "green")
    outcoming_message_dict.update({"source": "internal__messager"})
    outcoming_message_bytes = json.dumps(outcoming_message_dict).encode()
    connection = await aiormq.connect(AMQP_URI)
    channel = await connection.channel()
    await channel.basic_publish(outcoming_message_bytes, routing_key=f"{UNIQUE_PREFIX}:external__main:chat_message")
    await connection.close()


async def send_pow_message_to_internal_worker(outcoming_message_dict):
    cprint(f"AMQP PRODUCER:     send_pow_message_to_internal_worker {outcoming_message_dict}", "green")
    outcoming_message_dict.update({"source": "internal__messager"})
    outcoming_message_bytes = json.dumps(outcoming_message_dict).encode()
    connection = await aiormq.connect(AMQP_URI)
    channel = await connection.channel()
    await channel.basic_publish(outcoming_message_bytes,
                                routing_key=f"{UNIQUE_PREFIX}:internal__worker:pow_chat_message")
    await connection.close()

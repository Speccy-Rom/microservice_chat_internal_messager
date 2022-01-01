import aiormq
from termcolor import cprint

from consumer import methods
from settings import AMQP_URI
from settings import UNIQUE_PREFIX


async def consumer_subscriptions():
    connection = await aiormq.connect(AMQP_URI)
    channel = await connection.channel()
    cprint(f"AMQP CONSUMER:     ready [yes] PREFIX={UNIQUE_PREFIX}", "green")

    # cоздадим очередь, в которую будет отправлено сообщение
    # durable значит постоянная очередь (дословный перевод прочная)
    simple_message_queue__declared = await channel.queue_declare(f"{UNIQUE_PREFIX}:internal__messager:test_message",
                                                                 durable=False)
    # no_ack=True - сразу ответить брокеру что все ок, сообщение можно удалять из очереди
    await channel.basic_consume(simple_message_queue__declared.queue, methods.simple_message, no_ack=True)

    simple_message_with_ack_queue__declared = await channel.queue_declare(
        f"{UNIQUE_PREFIX}:internal__messager:test_message_with_ack", durable=False)
    # no_ack=False - поведение по умолчанию,
    # отвечаем принудительно в самом обработчике по мере выполенения (предпочитаемый вариант)
    await channel.basic_consume(simple_message_with_ack_queue__declared.queue, methods.simple_message_with_ack,
                                no_ack=False)
    # https://habr.com/ru/post/150134/

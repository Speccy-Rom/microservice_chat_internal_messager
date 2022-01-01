async def simple_message(message):
    print("simple_message :: Simple message body is: %r" % message.body)


async def simple_message_with_ack(message):
    print("simple_message_with_ack :: Simple message body is: %r" % message.body)
    await message.channel.basic_ack(message.delivery.delivery_tag)
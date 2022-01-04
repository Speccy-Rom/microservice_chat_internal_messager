import json
from producer import methods as producer_methods

async def simple_message(message):
    print("simple_message :: Simple message body is: %r" % message.body)


async def simple_message_with_ack(message):
    print("simple_message_with_ack :: Simple message body is: %r" % message.body)
    await message.channel.basic_ack(message.delivery.delivery_tag)


async def chat_message(message):

    incoming_message_dict = json.loads(message.body.decode())
    incoming_message = incoming_message_dict["message"]

    if len(incoming_message) > 5 and incoming_message[-4:] == "!pow":
        pass
    else:
        outcoming_message = incoming_message[::-1]

    outcoming_message_dict = {}
    outcoming_message_dict["username"] = "internal_messager"
    outcoming_message_dict["message"] = outcoming_message
    await producer_methods.send_message_to_external_main(outcoming_message_dict)
    await message.channel.basic_ack(message.delivery.delivery_tag)
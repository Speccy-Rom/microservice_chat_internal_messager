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

    if "!pow" in incoming_message and incoming_message_dict["source"] == "external__main":
        outcoming_message_dict = {}
        outcoming_message_dict["username"] = "internal_messager"
        outcoming_message_dict["message"] = incoming_message
        await producer_methods.send_pow_message_to_internal_worker(outcoming_message_dict)
        await message.channel.basic_ack(message.delivery.delivery_tag)
    else:
        if incoming_message_dict["source"] == "external__main":
            outcoming_message = incoming_message[::-1]
        elif incoming_message_dict["source"] == "internal__worker":
            outcoming_message = incoming_message
        outcoming_message_dict = {}
        outcoming_message_dict["username"] = "internal_messager"
        outcoming_message_dict["message"] = outcoming_message
        await producer_methods.send_message_to_external_main(outcoming_message_dict)
        await message.channel.basic_ack(message.delivery.delivery_tag)

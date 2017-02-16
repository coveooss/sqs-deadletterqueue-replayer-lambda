from __future__ import print_function

import boto3


def transfer_messages(source_queue, target_queue):
    total_messages_transferred = 0
    while True:
        messages = gather_messages(source_queue)
        if not messages:
            break
        total_messages_transferred += len(messages)
        send_messages(messages, target_queue)
        delete_messages(messages)
    print("In total " + str(total_messages_transferred) + " were transferred.")


def gather_messages(queue):
    messages = queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=20)
    print("Collected: " + str(len(messages)) + " messages.")
    return messages


def send_messages(messages, queue):
    entries = [dict(Id=str(i + 1), MessageBody=message.body) for i, message in enumerate(messages)]

    queue.send_messages(Entries=entries)


def delete_messages(messages):
    for message in messages:
        print("Copied " + str(message.body))
        message.delete()


def handle_message(event, context):
    sqs = boto3.resource(service_name='sqs')

    source_queue_name = event['source_queue_name']
    target_queue_name = event['target_queue_name']

    print("From: " + source_queue_name + " To: " + target_queue_name)

    if source_queue_name != target_queue_name + "-deadletter":
        print("Exiting because the source_queue_name is not the same as the target_queue_name with '-deadletter' at the end.")
        exit(1)

    source_queue = sqs.get_queue_by_name(QueueName=source_queue_name)
    target_queue = sqs.get_queue_by_name(QueueName=target_queue_name)

    transfer_messages(source_queue, target_queue)

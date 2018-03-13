import pprint

import boto3

# session = boto3.Session(profile_name='default')
# s3 = session.resource('s3')
#
# for bucket in s3.buckets.all():
#     print(bucket.name)

# Get the service resource
import time

sqs = boto3.resource('sqs')

# # Create the queue. This returns an SQS.Queue instance
# queue = sqs.create_queue(QueueName='test', Attributes={'DelaySeconds': '5'})
queue = sqs.get_queue_by_name(QueueName='test')

response = queue.send_message(MessageBody="init_message")
pprint.pprint(response)

# for i in range(1000):
#     response = queue.send_message(MessageBody="message %d" % i)

# Process messages by printing out body and optional author name
for message in queue.receive_messages(MaxNumberOfMessages=10):
    print("message: %s" % message.body)

    # Let the queue know that the message is processed
    message.delete()

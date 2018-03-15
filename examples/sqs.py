from pprint import pprint
from time import sleep

from src.aws.sqs import Item, Queue


def run():
    queue = Queue.get_by_name("test")

    for i in range(10):
        item = Item.from_text(
            "message %d" % i,
            attributes={"test_attribute": i}
        )
        queue.add(item)
        print("Message sent %d" % i)

    print("Waiting for messages to safely arrive.")
    sleep(1)

    for i in range(10):
        item = queue.pop()
        print("%d" % i)
        print("Item body:" + item.body)
        pprint(item.sqs_message_attributes)

    # items = queue.pop_many()
    # for item in items:
    #     print("Item body:" + item.body)
    #     pprint(item.sqs_message_attributes)


if __name__ == '__main__':
    run()

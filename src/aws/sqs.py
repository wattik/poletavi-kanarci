from abc import abstractmethod, ABC
from typing import Tuple, Dict, List

import boto3

from src.aws.exceptions import QueueEmpty


class SQS:
    __sqs = None

    @staticmethod
    def get_client():
        if SQS.__sqs is None:
            SQS.__sqs = boto3.resource('sqs')
        return SQS.__sqs


class Item(ABC):
    STRING_VALUE = "StringValue"
    DATA_TYPE = "DataType"

    @classmethod
    def from_text(cls, body: str, attributes=None):
        return AddItem(body=body, message_attributes=attributes)

    @property
    @abstractmethod
    def body(self):
        pass

    @property
    @abstractmethod
    def sqs_message_attributes(self):
        pass

    @property
    @abstractmethod
    def message_attributes(self):
        pass

    @staticmethod
    def _normalize(value: object) -> Tuple[str, object]:
        if isinstance(value, str):
            return "String", str(value)
        if isinstance(value, int):
            return "Number.int", str(value)
        if isinstance(value, float):
            return "Number.float", str(value)
        if isinstance(value, bool):
            return "String.bool", "true" if value else "false"

        raise ValueError("Value's type not recognized.")

    @staticmethod
    def _retype(data_type: str, value: str) -> object:
        if data_type == "String":
            return str(value)
        if data_type == "Number.int":
            return int(value)
        if data_type in ("Number", "Number.float"):
            return float(value)
        if data_type == "String.bool":
            return True if value == "true" else False

        raise ValueError("Data type not recognized.")

    @staticmethod
    def value_to_sqs_format(value) -> Dict[str, str]:
        data_type, string_value = Item._normalize(value)
        return {
            Item.STRING_VALUE: string_value,
            Item.DATA_TYPE: data_type
        }

    @staticmethod
    def value_from_sqs_format(value: Dict[str, str]) -> object:
        return Item._retype(value[Item.DATA_TYPE], value[Item.STRING_VALUE])


class AddItem(Item):
    def __init__(self, body, message_attributes=None):
        if message_attributes is None:
            message_attributes = {}

        self.__message_attributes = message_attributes
        self.__body = body

    @property
    def message_attributes(self):
        return self.__message_attributes

    @property
    def body(self):
        return self.__body

    @property
    def sqs_message_attributes(self):
        attributes = {}
        for key, value in self.message_attributes.items():
            attributes[key] = Item.value_to_sqs_format(value)

        return attributes


class ReceivedItem(Item):
    def __init__(self, sqs_message):
        self.__sqs_message = sqs_message

    @property
    def message_attributes(self):
        message_attributes = {}
        for key, value in self.sqs_message_attributes.items():
            message_attributes[key] = Item.value_from_sqs_format(value)

        return message_attributes

    @property
    def sqs_message_attributes(self):
        return self.__sqs_message.message_attributes

    @property
    def body(self):
        return self.__sqs_message.body


class Queue:
    def __init__(self, queue) -> None:
        self.queue = queue

    @classmethod
    def create_new(cls, name: str, attributes: dict = None) -> "Queue":
        if attributes is None:
            attributes = {}

        return Queue(SQS.get_client().create_queue(QueueName=name, Attributes=attributes))

    @classmethod
    def get_by_name(cls, name: str) -> "Queue":
        return Queue(SQS.get_client().get_queue_by_name(QueueName=name))

    def add(self, item: Item) -> dict:
        """
        :argument multiple
        response = queue.send_message(
        MessageBody='string',
        DelaySeconds=123,
        MessageAttributes={
            'string': {
                'StringValue': 'string',
                'BinaryValue': b'bytes',
                'StringListValues': [
                    'string',
                ],
                'BinaryListValues': [
                    b'bytes',
                ],
                'DataType': 'string'
            }
        },
        MessageDeduplicationId='string',
        MessageGroupId='string'
        )

        :return dict
        {
        'MD5OfMessageBody': 'string',
        'MD5OfMessageAttributes': 'string',
        'MessageId': 'string',
        'SequenceNumber': 'string'
        }
        """
        return self.queue.send_message(MessageBody=item.body, MessageAttributes=item.sqs_message_attributes)

    def pop(self) -> Item:
        messages = self.queue.receive_messages(MaxNumberOfMessages=1, MessageAttributeNames=["All"])
        if len(messages) == 0:
            raise QueueEmpty("Queue %s is `probably` empty." % self.queue.url)

        message = messages[0]  # list containing one message
        message.delete()
        return ReceivedItem(message)

    def pop_many(self) -> List[Item]:
        messages = self.queue.receive_messages(MaxNumberOfMessages=10, MessageAttributeNames=["All"])

        if len(messages) == 0:
            raise QueueEmpty("Queue %s is `probably` empty." % self.queue.url)

        items = []
        for message in messages:
            items.append(ReceivedItem(message))
            message.delete()

        return items

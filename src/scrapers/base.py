from abc import ABC, abstractmethod
from typing import NewType, Union, List, Dict

from src.aws.sqs import Queue, Item

# Unspecified Type produced by a scraper and consumed by a normalizer.
ScraperCustomDataStructure = NewType("ScraperCustomDataStructure", Union[dict, object])


class RecordNormalizer(ABC):
    @abstractmethod
    def normalize(self, data: ScraperCustomDataStructure) -> NormalizedRecord:
        pass


class NormalizedRecord:
    def __init__(self):
        self.id = None
        # todo: add all json fields here

    def to_dict(self) -> Dict[str, Dict[str, str]]:
        # todo
        pass


class ScraperBase(ABC):
    @abstractmethod
    def scrape(self) -> List[ScraperCustomDataStructure]:
        pass


class ScraperRunner(ABC):
    def __init__(self, scraper: ScraperBase, data_normalizer: RecordNormalizer, queue_name: str) -> None:
        self.data_normalizer = data_normalizer
        self.scraper = scraper
        self.queue = Queue.get_by_name(queue_name)

    def run(self):
        while True:
            for chop in self.scraper.scrape():
                normalized_data = self.data_normalizer.normalize(chop)
                self.send(normalized_data)

    def send(self, record: NormalizedRecord):
        body = ""  # todo: what is a body?
        item = Item.from_text(body, record.to_dict())
        self.queue.add(item)

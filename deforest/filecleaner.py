import logging
from Queue import Queue
from tags import GetAttTag, SubTag, RefTag
import yaml
from cleaners import DefaultCleaner, CloudFormationCleaner, IgnoreCleaner
import sys
from constant import EXIT_PARSEERR


class ForestCleaner:
    cleaner_queue = None
    _result = None
    _allow_ignored = False

    def __init__(self, data):
        logging.debug("received {} bytes of data to clean".format(len(data)))
        self.data = data
        self._parse_data()

    def _parse_data(self):
        self._enable_cf_tags()
        logging.debug("parsing yaml")
        try:
            self.result = yaml.safe_load(self.data)
        except yaml.scanner.ScannerError as e:
            logging.error("could not parse file: {}".format(e))
            sys.exit(EXIT_PARSEERR)

    def _create_queue(self):
        logging.debug("creating cleaner queue")
        cleaner_queue = Queue()
        logging.debug("created queue with size {}".format(
            cleaner_queue.qsize()))

        cleaner_queue.put(CloudFormationCleaner(self))

        cleaner_queue.put(DefaultCleaner(self))

        if not self.allow_ignored:
            cleaner_queue.put(IgnoreCleaner(self))
        else:
            logging.info("allowing x-deforest-ignore paths")
        self.cleaner_queue = cleaner_queue

    def clean(self):
        self._create_queue()
        while not self.cleaner_queue.empty():
            self.cleaner_queue.get().clean()
        return self.result

    def _enable_cf_tags(self):
        logging.debug("enabling CF tags")
        yaml.SafeLoader.add_constructor('!GetAtt', GetAttTag.from_yaml)
        yaml.SafeLoader.add_constructor('!Sub', SubTag.from_yaml)
        yaml.SafeLoader.add_constructor('!Ref', RefTag.from_yaml)
        yaml.SafeDumper.add_multi_representer(GetAttTag, GetAttTag.to_yaml)
        yaml.SafeDumper.add_multi_representer(SubTag, SubTag.to_yaml)
        yaml.SafeDumper.add_multi_representer(RefTag, RefTag.to_yaml)

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value):
        self._result = value

    @property
    def allow_ignored(self):
        return self._allow_ignored

    @allow_ignored.setter
    def allow_ignored(self, value):
        self._allow_ignored = value

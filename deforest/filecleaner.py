from Queue import Queue
import logging
import sys

import yaml

import cleaners
import tags
import cleaners
import constant


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
            sys.exit(constant.EXIT_PARSEERR)

    def _create_queue(self):
        logging.debug("creating cleaner queue")
        cleaner_queue = Queue()
        logging.debug("created queue with size {}".format(
            cleaner_queue.qsize()))

        cleaner_queue.put(cleaners.CloudFormationCleaner(self))

        cleaner_queue.put(cleaners.DefaultCleaner(self))

        if not self.allow_ignored:
            cleaner_queue.put(cleaners.IgnoreCleaner(self))
        else:
            logging.info("allowing x-deforest-ignore paths")
        logging.debug(
            "cleaning will use {} methods".format(cleaner_queue.qsize()))
        self.cleaner_queue = cleaner_queue

    def clean(self):
        self._create_queue()
        while not self.cleaner_queue.empty():
            self.cleaner_queue.get().clean()
        return self.result

    def _enable_cf_tags(self):
        logging.debug("enabling CF tags")
        aws_tags = ["!GetAtt", "!Sub", "!Ref", "!Base64", "!Cidr", "!ImportValue", "!GetAZs", "!FindInMap",
                    "!Join", "!Select", "!Split", "!Transform", "!And", "!Equals", "!If", "!Not", "!Or"]
        for t in aws_tags:
            yaml.SafeLoader.add_constructor(t, tags.AWSTag.from_yaml)
            yaml.SafeDumper.add_multi_representer(
                tags.AWSTag, tags.AWSTag.to_yaml)
        logging.debug("enabled {} tags".format(len(aws_tags)))

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

import logging
import re
import json
import yaml


class FileCreator:
    _format = "yaml"
    _indent = 4
    _filename = None

    def __init__(self, data):
        logging.debug("creating {}".format(self))
        self.data = data

    def write_to_file(self):
        logging.debug("writing {} results to file, format setting: {}".format(
            len(self.data), self.format))

        if len(self.data) > 1 and self.filename is not None:
            logging.warning(
                "using default deforest filenaming conventions since the output constists of more than one file")
            self.filename = None

        for d in self.data:
            fname = self.filename
            if self.filename is None:
                logging.debug("setting filename {}".format(self._filename(d)))
                fname = self._filename(d)
            with open(fname, "w+") as fh:
                if self.format == "json":
                    fh.write(json.dumps(d, indent=self.indent))
                else:
                    yd = yaml.safe_dump(d)
                    fh.write(yd)
            logging.info("saved to file {}".format(fname))

    def _filename(self, content):
        title = content["info"]["title"] or "no-title"
        version = content["info"]["version"] or "no-version"
        s = "{}-{}.{}".format(title.lower(), version.lower(), self.format)
        s = re.sub(r"\s+", '-', s)
        return s

    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, value):
        self._format = value

    @property
    def indent(self):
        return self._indent

    @indent.setter
    def indent(self, value):
        self._indent = value

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value

from tags import GetAttTag, SubTag, RefTag
import yaml
import re

class DeforestCleaner():
    keys = ["x-amazon"]
    filedata = None
    raw = {}
    processed = None

    def __init__(self, data):
        self.filedata = data

    def _namify(self, title, version):
        s = "{}-{}".format(title.lower(),version.lower())
        s = re.sub(r"\s+", '-', s)
        return s

    def get_title_and_version(self):
        title = self.raw["info"]["title"] or "no-title"
        version = self.raw["info"]["version"] or "no-version"
        return self._namify(title,version)

    def get_raw(self):
        return self.raw

    def convert(self):
        self._enable_custom_tags()
        self._load()
        self._clean_all_keys()
        self._dump()
        return self.processed

    def _clean_all_keys(self):
        self._cleanup_keys(self.raw)

    def _cleanup_keys(self, v):
        for k in v.keys():
            if any(m in k for m in self.keys):
                del v[k]
            else:
                if isinstance(v[k], dict):
                    self._cleanup_keys(v[k])

    def _enable_custom_tags(self):
        yaml.SafeLoader.add_constructor('!GetAtt', GetAttTag.from_yaml)
        yaml.SafeLoader.add_constructor('!Sub', SubTag.from_yaml)
        yaml.SafeLoader.add_constructor('!Ref', RefTag.from_yaml)
        yaml.SafeDumper.add_multi_representer(GetAttTag, GetAttTag.to_yaml)
        yaml.SafeDumper.add_multi_representer(SubTag, SubTag.to_yaml)
        yaml.SafeDumper.add_multi_representer(RefTag, RefTag.to_yaml)

    def _load(self):
        self.raw = yaml.safe_load(self.filedata)

    def _dump(self):
        self.processed = yaml.safe_dump(self.raw)

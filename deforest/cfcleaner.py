from tags import GetAttTag, SubTag, RefTag
import yaml
import re

class CFCleaner():
  keys = ["x-amazon"]
  filedata = None
  raw = {}
  processed = None
  KEY_TYPE = "Type"
  KEY_RESOURCES = "Resources"
  KEY_PROPERTIES = "Properties"
  KEY_BODY = "Body"
  TYPE_APIGW = "AWS::ApiGateway::RestApi"

  multi_raw = []
  multi_processed = []

  def __init__(self,data):
    self.filedata = data

  def convert(self):
    self._enable_custom_tags()
    self._load()
    self._clean_all_keys()
    self._dump_all()
    return self.multi_processed

  def number_results(self):
    return len(self.multi_processed)

  def _clean_all_keys(self):
    self._identify_apigw(self.raw)

  def _identify_apigw(self,v):
    resources = v[CFCleaner.KEY_RESOURCES]
    for k in resources:
      if isinstance(resources[k], dict):
        if self._is_apigw(resources[k]) and self._has_properties_and_body(resources[k]):
          self.multi_raw.append(resources[k][CFCleaner.KEY_PROPERTIES][CFCleaner.KEY_BODY])

    for raw in self.multi_raw:
      self._cleanup_keys(raw)

  def _cleanup_keys(self,v):
    for k in v.keys():
      if any(m in k for m in self.keys):
        del v[k]
      else:
        if isinstance(v[k], dict):
          self._cleanup_keys(v[k])

  def _is_apigw(self,node):
    if CFCleaner.KEY_TYPE in node:
      if node[CFCleaner.KEY_TYPE] == CFCleaner.TYPE_APIGW:
        return True
    return False

  def _has_properties_and_body(self,node):
    return CFCleaner.KEY_PROPERTIES in node and CFCleaner.KEY_BODY in node[CFCleaner.KEY_PROPERTIES]

  def _namify(self, title, version):
    s = "{}-{}".format(title.lower(),version.lower())
    s = re.sub(r"\s+", '-', s)
    return s

  def get_title_and_version_all(self,index):
    title = self.multi_raw[index]["info"]["title"] or "no-title"
    version = self.multi_raw[index]["info"]["version"] or "no-version"
    return self._namify(title,version)

  def get_title_and_version(self):
    return self.get_title_and_version(0)

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
    self.processed = yaml.safe_dump(self.multi_raw[0])

  def _dump_all(self):
    for r in self.multi_raw:
      self.multi_processed.append(yaml.safe_dump(r))
  
  def get_raw(self,index):
    return self.multi_raw[0]

  def get_raw_all(self,index):
    return self.multi_raw[index]
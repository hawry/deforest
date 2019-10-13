from tags import GetAttTag, SubTag, RefTag
import yaml
import re
from cleaner import DeforestCleaner
from cfcleaner import CFCleaner

class Solution():
  raw = {}
  filedata = None
  processed = None
  
  def __init__(self, data):
    self.filedata = data
  
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

  def cleaner(self):
    self._enable_custom_tags()
    self._load()
    cleaner = self._identify_cleaner()
    if cleaner is "default":
      return DeforestCleaner(self.filedata)
    if cleaner is "cloudformation":
      return CFCleaner(self.filedata)
    
  def _identify_cleaner(self):
    if "AWSTemplateFormatVersion" in self.raw:
      return "cloudformation"
    return "default"
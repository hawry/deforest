import yaml


class AWSTag(yaml.YAMLObject):
    def __init__(self, var):
        self.var = var

    def __repr__(self):
        return self.var

    @classmethod
    def from_yaml(cls, loader, node):
        return cls(node.value)

    @classmethod
    def to_yaml(cls, dumper, data):
        return ''

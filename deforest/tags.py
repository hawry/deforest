import yaml

class GetAttTag(yaml.YAMLObject):
    tag = u'!GetAtt'

    def __init__(self, var):
        self.var = var

    def __repr__(self):
        return self.var

    @classmethod
    def from_yaml(cls, loader, node):
        return GetAttTag(node.value)

    @classmethod
    def to_yaml(cls, dumper, data):
        return ''

class SubTag(yaml.YAMLObject):
    tag = u'!Sub'

    def __init__(self, var):
        self.var = var

    def __repr__(self):
        return self.var

    @classmethod
    def from_yaml(cls, loader, node):
        return SubTag(node.value)

    @classmethod
    def to_yaml(cls, dumper, data):
        return ''

class RefTag(yaml.YAMLObject):
    tag = u'!Ref'

    def __init__(self, var):
        self.var = var

    def __repr__(self):
        return self.var

    @classmethod
    def from_yaml(cls, loader, node):
        return RefTag(node.value)

    @classmethod
    def to_yaml(cls, dumper, data):
        return ''

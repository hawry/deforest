import unittest
import deforest.tags as tags


class TestAWSTag(unittest.TestCase):
    sut = tags.AWSTag('!GetAtt')

    def test_init(self):
        assert self.sut.var == '!GetAtt'

    def test_repr(self):
        assert repr(self.sut) == '!GetAtt'

    def test_to_yaml(self):
        assert tags.AWSTag.to_yaml(None, None) == ''

    def test_from_yaml(self):
        class a:
            value = 'hello'
        actual = tags.AWSTag.from_yaml(None, a)
        assert type(actual) is tags.AWSTag
        assert actual.var == 'hello'

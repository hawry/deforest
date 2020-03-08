import unittest
from deforest.deforest import deforest


class TestImportableMethods(unittest.TestCase):
    def test_invalid_format(self):
        input = {"AWSTemplateFormatVersion": "2010-09-09", "Description": "a sample template",
                       "Resources": {"MyRestApi": {"Type": "AWS::ApiGateway::RestApi", "Properties": {
                           "Body": {
                               "swagger": "2.0", "info": {"title": "a title", "version": "0.1"}
                           }
                       }}}}
        with self.assertRaises(ValueError) as e:
            deforest(input, fmt='invalid')

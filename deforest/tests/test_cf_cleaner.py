import unittest
import deforest.cleaners as cleaner


class TestCFCleaner(unittest.TestCase):
    result = None

    def test_clean_no_cf(self):
        self.result = {"swagger": "2.0", "info": {
            "title": "This is a title", "version": "1.0"}, "x-amazon-apigateway-request-validators": {"all": {"validateRequestBody": True, "validateRequestParameters": True}}}
        sut = cleaner.CloudFormationCleaner(self)
        sut.clean()
        assert "x-amazon-apigateway-request-validators" in self.result[0]

    def test_clean_cf_removed(self):
        self.result = {"AWSTemplateFormatVersion": "2010-09-09", "Description": "a sample template", "Resources": {"MyRestApi": {"Type": "AWS::ApiGateway::RestApi", "Properties": {
            "Body": {
                "swagger": "2.0", "info": {"title": "a title", "version": "0.1"}
            }
        }}}}
        sut = cleaner.CloudFormationCleaner(self)
        sut.clean()
        assert "AWSTemplateFormatVersion" not in self.result[0]
        assert "info" in self.result[0]
        assert len(self.result) == 1

    def test_clean_cf_two_apis(self):
        self.result = {"AWSTemplateFormatVersion": "2010-09-09", "Description": "a sample template", "Resources": {"MyRestApi": {"Type": "AWS::ApiGateway::RestApi", "Properties": {
            "Body": {
                "swagger": "2.0", "info": {"title": "a title", "version": "0.1"}
            }
        }}, "MySecondsRestApi": {"Type": "AWS::ApiGateway::RestApi", "Properties": {"Body": {"swagger": "2.0", "info": {"title": "second api"}}}}}}
        sut = cleaner.CloudFormationCleaner(self)
        sut.clean()

        assert len(self.result) == 2
        assert "AWSTemplateFormatVersion" not in self.result[0]
        assert "AWSTemplateFormatVersion" not in self.result[1]
        assert "info" in self.result[0]
        assert "swagger" in self.result[1]

    def test_clean_cf_ignore_invalid_api(self):
        self.result = {"AWSTemplateFormatVersion": "2010-09-09", "Description": "a sample template", "Resources": {"MyRestApi": {"Type": "AWS::ApiGateway::RestApi", "Properties": {
            "Body": {
                "swagger": "2.0", "info": {"title": "a title", "version": "0.1"}
            }
        }}, "MySecondsRestApi": {"NotType": "AWS::ApiGateway::RestApi", "Properties": {"Body": {"swagger": "2.0", "info": {"title": "second api"}}}}}}
        sut = cleaner.CloudFormationCleaner(self)
        sut.clean()

        assert len(self.result) == 1
        assert "AWSTemplateFormatVersion" not in self.result[0]
        assert "info" in self.result[0]

    def test_clean_cf_serverless_api(self):
        self.result = {"AWSTemplateFormatVersion": "2010-09-09", "Description": "a sample template", "Resources": {"MyRestApi": {"Type": "AWS::Serverless::Api", "Properties": {
            "DefinitionBody": {
                "swagger": "2.0", "info": {"title": "a title", "version": "0.1"}
            }
        }}}}
        sut = cleaner.CloudFormationCleaner(self)
        sut.clean()
        assert "AWSTemplateFormatVersion" not in self.result[0]
        assert "info" in self.result[0]
        assert len(self.result) == 1

    def test_clean_cf_missing_body(self):
        self.result = {"AWSTemplateFormatVersion": "2010-09-09", "Description": "a sample template", "Resources": {"MyRestApi": {"Type": "AWS::Serverless::Api", "Properties": {
            "InvalidBody": {
                "swagger": "2.0", "info": {"title": "a title", "version": "0.1"}
            }
        }}}}
        sut = cleaner.CloudFormationCleaner(self)
        with self.assertRaises(cleaner.InvalidBodyProperty) as e:
            sut.clean()
            self.assertEqual('could not find a valid body property', str(e.exception))

    def test_clean_cf_and_srvless_apis(self):
        self.result = {"AWSTemplateFormatVersion": "2010-09-09", "Description": "a sample template", "Resources": {"MyRestApi": {"Type": "AWS::ApiGateway::RestApi", "Properties": {
            "Body": {
                "swagger": "2.0", "info": {"title": "a title", "version": "0.1"}
            }
        }}, "MySecondsRestApi": {"Type": "AWS::Serverless::Api", "Properties": {"DefinitionBody": {"swagger": "2.0", "info": {"title": "second api"}}}}}}
        sut = cleaner.CloudFormationCleaner(self)
        sut.clean()

        assert len(self.result) == 2
        assert "AWSTemplateFormatVersion" not in self.result[0]
        assert "AWSTemplateFormatVersion" not in self.result[1]
        assert "info" in self.result[0]
        assert "swagger" in self.result[1]

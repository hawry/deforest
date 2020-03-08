import unittest
import json
from deforest.deforest import deforest


class TestImportableMethods(unittest.TestCase):
    raw_file_input = """
AWSTemplateFormatVersion: "2010-09-09"
Description: A sample template
Parameters:
  HelloWorld:
    Type: String
Resources:
  MyEC2Instance: #An inline comment
    Type: "AWS::EC2::Instance"
    Properties:
      ImageId: "ami-0ff8a91507f77f867" #Another comment -- This is a Linux AMI
      InstanceType: t2.micro
      KeyName: testkey
      BlockDeviceMappings:
        - DeviceName: /dev/sdm
          Ebs:
            VolumeType: io1
            Iops: 200
            DeleteOnTermination: false
            VolumeSize: 20
  MyRestApi:
    Type: AWS::ApiGateway::RestApi
    Properties:
      Description: "This is a description"
      Body:
        swagger: "2.0"
        info:
          title: ReqValidators Sample
          version: 1.0.0
        schemes:
          - https
        basePath: "/v1"
        produces:
          - application/json
        x-amazon-apigateway-request-validators:
          all:
            validateRequestBody: true
            validateRequestParameters: true
          params-only:
            validateRequestBody: false
            validateRequestParameters: true
        x-amazon-apigateway-request-validator: params-only
        paths:
          "/validation":
            post:
              x-amazon-apigateway-request-validator: all
              parameters:
                - in: header
                  name: h1
                  required: true
                - in: body
                  name: RequestBodyModel
                  required: true
                  schema:
                    "$ref": "#/definitions/RequestBodyModel"
              responses:
                "200":
                  schema:
                    type: array
                    items:
                      "$ref": "#/definitions/Error"
                  headers:
                    test-method-response-header:
                      type: string
              security:
                - api_key: []
              x-amazon-apigateway-auth:
                type: none
              x-amazon-apigateway-integration:
                type: http
                uri: !Sub "${RegionalPrefix}-http://petstore-demo-endpoint.execute-api.com/petstore/pets"
                httpMethod: POST
                requestParameters:
                  integration.request.header.custom_h1: method.request.header.h1
                responses:
                  2\d{2}:
                    statusCode: "200"
                  default:
                    statusCode: "400"
                    responseParameters:
                      method.response.header.test-method-response-header: "'static value'"
                    responseTemplates:
                      application/json: json 400 response template
                      application/xml: xml 400 response template
            get:
              parameters:
                - name: q1
                  in: query
                  required: true
              responses:
                "200":
                  schema:
                    type: array
                    items:
                      "$ref": "#/definitions/Error"
                  headers:
                    test-method-response-header:
                      type: string
              security:
                - api_key: []
              x-amazon-apigateway-auth:
                type: none
              x-amazon-apigateway-integration:
                type: http
                uri: !GetAtt HelloWorld.Arn
                httpMethod: GET
                requestParameters:
                  integration.request.querystring.type: method.request.querystring.q1
                responses:
                  2\d{2}:
                    statusCode: "200"
                  default:
                    statusCode: "400"
                    responseParameters:
                      method.response.header.test-method-response-header: "'static value'"
                    responseTemplates:
                      application/json: json 400 response template
                      application/xml: xml 400 response template
        definitions:
          RequestBodyModel:
            type: object
            properties:
              id:
                type: integer
              type:
                type: string
                enum:
                  - dog
                  - cat
                  - fish
              name:
                type: string
              price:
                type: number
                minimum: 25
                maximum: 500
            required:
              - type
              - name
              - price
          Error:
            type: object
            properties: {}
  MySecondRestAPI:
    Type: AWS::ApiGateway::RestApi
    Properties:
      Description: "This is a description"
      Body:
        swagger: "2.0"
        info:
          title: The second REST API sample
          version: 1.0.1
        schemes:
          - https
        basePath: "/v1"
        produces:
          - application/json
        x-amazon-apigateway-request-validators:
          all:
            validateRequestBody: true
            validateRequestParameters: true
          params-only:
            validateRequestBody: false
            validateRequestParameters: true
        x-amazon-apigateway-request-validator: params-only
        paths:
          "/validation":
            post:
              x-amazon-apigateway-request-validator: all
              parameters:
                - in: header
                  name: h1
                  required: true
                - in: body
                  name: RequestBodyModel
                  required: true
                  schema:
                    "$ref": "#/definitions/RequestBodyModel"
              responses:
                "200":
                  schema:
                    type: array
                    items:
                      "$ref": "#/definitions/Error"
                  headers:
                    test-method-response-header:
                      type: string
              security:
                - api_key: []
              x-amazon-apigateway-auth:
                type: none
              x-amazon-apigateway-integration:
                type: http
                uri: !Sub "${RegionalPrefix}-http://petstore-demo-endpoint.execute-api.com/petstore/pets"
                httpMethod: POST
                requestParameters:
                  integration.request.header.custom_h1: method.request.header.h1
                responses:
                  2\d{2}:
                    statusCode: "200"
                  default:
                    statusCode: "400"
                    responseParameters:
                      method.response.header.test-method-response-header: "'static value'"
                    responseTemplates:
                      application/json: json 400 response template
                      application/xml: xml 400 response template
            get:
              parameters:
                - name: q1
                  in: query
                  required: true
              responses:
                "200":
                  schema:
                    type: array
                    items:
                      "$ref": "#/definitions/Error"
                  headers:
                    test-method-response-header:
                      type: string
              security:
                - api_key: []
              x-amazon-apigateway-auth:
                type: none
              x-amazon-apigateway-integration:
                type: http
                uri: !GetAtt HelloWorld.Arn
                httpMethod: GET
                requestParameters:
                  integration.request.querystring.type: method.request.querystring.q1
                responses:
                  2\d{2}:
                    statusCode: "200"
                  default:
                    statusCode: "400"
                    responseParameters:
                      method.response.header.test-method-response-header: "'static value'"
                    responseTemplates:
                      application/json: json 400 response template
                      application/xml: xml 400 response template
        definitions:
          RequestBodyModel:
            type: object
            properties:
              id:
                type: integer
              type:
                type: string
                enum:
                  - dog
                  - cat
                  - fish
              name:
                type: string
              price:
                type: number
                minimum: 25
                maximum: 500
            required:
              - type
              - name
              - price
          Error:
            type: object
            properties: {}
"""

    parsed = {'swagger': '2.0', 'info': {'title': 'The second REST API sample', 'version': '1.0.1'}, 'definitions': {'Error': {'type': 'object', 'properties': {}}, 'RequestBodyModel': {'type': 'object', 'properties': {'id': {'type': 'integer'}, 'type': {'type': 'string', 'enum': ['dog', 'cat', 'fish']}, 'name': {'type': 'string'}, 'price': {'type': 'number', 'minimum': 25, 'maximum': 500}}, 'required': ['type', 'name', 'price']}}, 'basePath': '/v1', 'paths': {'/validation': {'post': {'security': [{'api_key': []}], 'parameters': [{'in': 'header', 'name': 'h1', 'required': True}, {'in': 'body', 'name': 'RequestBodyModel', 'schema': {'$ref': '#/definitions/RequestBodyModel'}, 'required': True}], 'responses': {'200': {'headers': {'test-method-response-header': {'type': 'string'}}, 'schema': {'items': {'$ref': '#/definitions/Error'}, 'type': 'array'}}}}, 'get': {'security': [{'api_key': []}], 'parameters': [{'name': 'q1', 'in': 'query', 'required': True}], 'responses': {'200': {'headers': {'test-method-response-header': {'type': 'string'}}, 'schema': {'items': {'$ref': '#/definitions/Error'}, 'type': 'array'}}}}}}, 'schemes': ['https'], 'produces': ['application/json']}, {'swagger': '2.0', 'info': {'title': 'ReqValidators Sample', 'version': '1.0.0'}, 'definitions': {'Error': {'type': 'object', 'properties': {}}, 'RequestBodyModel': {'type': 'object', 'properties': {'id': {'type': 'integer'}, 'type': {'type': 'string', 'enum': ['dog', 'cat', 'fish']}, 'name': {'type': 'string'}, 'price': {'type': 'number', 'minimum': 25, 'maximum': 500}}, 'required': ['type', 'name', 'price']}}, 'basePath': '/v1', 'paths': {'/validation': {'post': {'security': [{'api_key': []}], 'parameters': [{'in': 'header', 'name': 'h1', 'required': True}, {'in': 'body', 'name': 'RequestBodyModel', 'schema': {'$ref': '#/definitions/RequestBodyModel'}, 'required': True}], 'responses': {'200': {'headers': {'test-method-response-header': {'type': 'string'}}, 'schema': {'items': {'$ref': '#/definitions/Error'}, 'type': 'array'}}}}, 'get': {'security': [{'api_key': []}], 'parameters': [{'name': 'q1', 'in': 'query', 'required': True}], 'responses': {'200': {'headers': {'test-method-response-header': {'type': 'string'}}, 'schema': {'items': {'$ref': '#/definitions/Error'}, 'type': 'array'}}}}}}, 'schemes': ['https'], 'produces': ['application/json']}

    def test_invalid_format(self):
        with self.assertRaises(ValueError) as e:
            deforest(self.raw_file_input, fmt='invalid')

    def test_valid_format(self):
        output = deforest(self.raw_file_input)
        self.maxDiff = None
        self.assertEqual(json.dumps(output, sort_keys=True), json.dumps(self.parsed, sort_keys=True))
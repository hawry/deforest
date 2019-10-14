import logging


class CloudFormationCleaner:
    KEY_CF_FIELD = "AWSTemplateFormatVersion"
    KEY_CF_RESOURCES = "Resources"
    KEY_CF_BODY = "Body"
    KEY_CF_TYPE = "Type"
    KEY_CF_PROPERTIES = "Properties"
    CF_APIGW_TYPE = "AWS::ApiGateway::RestApi"

    def __init__(self, caller):
        logging.debug("created {}".format(self))
        self.caller = caller

    def clean(self):
        logging.debug("{} clean".format(self))
        if not CloudFormationCleaner.KEY_CF_FIELD in self.caller.result:
            self.caller.result = [self.caller.result]
            return
        rval = []
        copy = self.caller.result
        res = copy[CloudFormationCleaner.KEY_CF_RESOURCES]
        for k in res:
            if isinstance(res[k], dict):
                if self._is_apigw(res[k]) and self._has_body(res[k]):
                    logging.info(
                        "identified resource '{}' as an API Gateway".format(k))
                    rval.append(
                        res[k][CloudFormationCleaner.KEY_CF_PROPERTIES][CloudFormationCleaner.KEY_CF_BODY])
        self.caller.result = rval

    def _is_apigw(self, node):
        if CloudFormationCleaner.KEY_CF_TYPE in node:
            return node[CloudFormationCleaner.KEY_CF_TYPE] == CloudFormationCleaner.CF_APIGW_TYPE
        return False

    def _has_body(self, node):
        return CloudFormationCleaner.KEY_CF_PROPERTIES in node and CloudFormationCleaner.KEY_CF_BODY in node[CloudFormationCleaner.KEY_CF_PROPERTIES]

    def __str__(self):
        return "CloudFormationCleaner"


class DefaultCleaner:
    keys = ["x-amazon"]
    copy = None

    def __init__(self, caller):
        logging.debug("created {}".format(self))
        self.caller = caller

    def clean(self):
        logging.debug("{} clean".format(self))
        self.copy = self.caller.result
        for i in self.copy:
            self._clean(i)
        self.caller.result = self.copy

    def _clean(self, v):
        for k in v.keys():
            if any(m in k for m in self.keys):
                del v[k]
            else:
                if isinstance(v[k], dict):
                    self._clean(v[k])

    def __str__(self):
        return "DefaultCleaner"


class IgnoreCleaner:
    DEFOREST_IGNORE_KEY = "x-deforest-ignore"
    copy = None

    def __init__(self, caller):
        logging.debug("created {}".format(self))
        self.caller = caller

    def clean(self):
        self.copy = self.caller.result
        for i in self.copy:
            self._clean(i)
        self.caller.result = self.copy

    def _clean(self, v):
        for k in v.keys():
            if isinstance(v[k], dict):
                if IgnoreCleaner.DEFOREST_IGNORE_KEY in v[k]:
                    if v[k][IgnoreCleaner.DEFOREST_IGNORE_KEY] is True:
                        del v[k]
                else:
                    self._clean(v[k])

    def __str__(self):
        return "IgnoreCleaner"

import deforest.cleaners as cleaner


class TestIgnoreCleaner:

    def test_clean_(self):
        data = {"info": {"title": "hello world"}, "paths": {
            "/validations": {"post": {"x-amazon-apigateway-request-validator": "all", "x-deforest-ignore": True}, "get": {"parameters": "something", "x-amazon-something": {"this": "is a child"}}}
        }}
        expected = {"info": {"title": "hello world"}, "paths": {
            "/validations": {"post": {"x-deforest-ignore": True}, "get": {"parameters": "something"}}
        }}
        self.result = [data]
        sut = cleaner.DefaultCleaner(self)
        sut.clean()
        assert len(self.result) == 1
        assert self.result[0] == expected

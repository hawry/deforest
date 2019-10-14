import deforest.cleaners as cleaner


class TestIgnoreCleaner:
    def test_clean_no_ignore(self):
        data = {"info": {"title": "hello world"}, "paths": {
            "/validations": {"post": {"x-amazon-apigateway-request-validator": "all"}}
        }}
        self.result = [data]
        sut = cleaner.IgnoreCleaner(self)
        sut.clean()
        assert len(self.result) == 1
        assert self.result[0] == data

    def test_clean_with_ignore(self):
        data = {"info": {"title": "hello world"}, "paths": {
            "/validations": {"post": {"x-amazon-apigateway-request-validator": "all", "x-deforest-ignore": True}, "get": {"parameters": "something"}}
        }}
        expected = {"info": {"title": "hello world"}, "paths": {
            "/validations": {"get": {"parameters": "something"}}}
        }
        self.result = [data]
        sut = cleaner.IgnoreCleaner(self)
        sut.clean()
        assert len(self.result) == 1
        assert self.result[0] == expected

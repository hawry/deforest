from mock import patch, mock_open
import pytest

from deforest.filecreator import FileCreator


class TestFileCreator:
    @pytest.mark.parametrize("fmt", [("yaml"), ("json")])
    def test_filename(self, fmt):
        sut = FileCreator(None)
        sut.format = fmt
        content = {"info": {"title": "hello world", "version": "1.0"}}
        actual = sut._filename(content)

        assert actual == "hello-world-1.0." + fmt

    def test_write_to_file(self):
        content = {"info": {"title": "hello world", "version": "1.0"}}
        fname = "thisisafilename.yaml"
        sut = FileCreator(content)
        open_mock = mock_open()
        sut.filename = fname
        with patch("deforest.filecreator.open", open_mock, create=True):
            sut.write_to_file()

        open_mock.assert_called_with(fname, "w+")

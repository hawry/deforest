import unittest
from parameterized import parameterized
from unittest.mock import patch, mock_open
from deforest.filecreator import FileCreator


class TestFileCreator(unittest.TestCase):
    @parameterized.expand([["yaml"], ["json"]])
    def test_filename(self, fmt):
        sut = FileCreator(None)
        sut.format = fmt
        content = {"info": {"title": "hello world", "version": "1.0"}}
        actual = sut._specify_filename(content)

        assert actual == "hello-world-1.0." + fmt

    @parameterized.expand([["yaml"], ["json"]])
    def test_write_to_file(self, fmt):
        content = {"info": {"title": "hello world", "version": "1.0"}}
        fname = "thisisafilename.{}".format(fmt)
        sut = FileCreator(content)
        open_mock = mock_open()
        sut.format = fmt
        sut.filename = fname
        with patch("deforest.filecreator.open", open_mock, create=True):
            sut.write_to_file()

        open_mock.assert_called_with(fname, "w+")

    @parameterized.expand([["yaml"], ["json"]])
    def test_write_to_file_assumed_filename(self, fmt):
        content = [{"info": {"title": "hello world", "version": "1.0"}}]
        expected = "hello-world-1.0.{}".format(fmt)
        open_mock = mock_open()
        sut = FileCreator(content)
        sut.format = fmt
        with patch("deforest.filecreator.open", open_mock, create=True):
            sut.write_to_file()
        open_mock.assert_called_with(expected, "w+")

    @parameterized.expand([[1], [2], [3], [4], [6], [8]])
    def test_indent_property(self, indent):
        sut = FileCreator(None)
        sut.indent = indent
        assert sut.indent == indent

    @parameterized.expand([["yaml"], ["json"]])
    def test_format_property(self, fmt):
        sut = FileCreator(None)
        sut.format = fmt
        assert sut.format == fmt

    @parameterized.expand([["afilename"], ["anotherfilename"]])
    def test_filename_property(self, fname):
        sut = FileCreator(None)
        sut.filename = fname
        assert sut.filename == fname

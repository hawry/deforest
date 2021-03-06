import logging
import click
import sys
import coloredlogs
from .constant import LOGGER, EXIT_NOTFOUND
from .filecleaner import ForestCleaner
from .filecreator import FileCreator


@click.command()
@click.argument("infile")
@click.option("--outfile", "-o", help="specify output file, default is ./<title>-<version>.<format>, ignored if input "
                                      "is a CloudFormation template and the template contains more than one "
                                      "ApiGateway resource)")
@click.option("--format", "-f", "fmt", default="yaml", show_default=True, type=click.Choice(["yaml", "json"]), help="output "
                                                                                                             "format")
@click.option("--indent", "-i", default=4, type=int, help="if output format is json, specify indentation")
@click.option("--debug", "-d", default=False, is_flag=True, help="if enabled, show debug logs")
@click.option("--no-ignore", default=False, is_flag=True, help="if set, deforest will export paths marked as ignored")
@click.version_option()
def main(infile, outfile, fmt, indent, debug, no_ignore):
    set_log_level(debug)
    logging.debug("parsing file '{}'".format(infile))
    d = read_file(infile)
    logging.debug("read {} bytes from file".format(len(d)))

    f = ForestCleaner(d)
    f.allow_ignored = no_ignore
    cleaned = f.clean()

    logging.debug("expected output {} files".format(len(cleaned)))

    fw = FileCreator(cleaned)
    fw.format = fmt
    fw.filename = outfile
    fw.write_to_file()


def deforest_file(raw_file, **kwargs):
    allow_ignored = kwargs.get("allow_ignored", False)
    f = ForestCleaner(raw_file)
    f.allow_ignored = allow_ignored
    cleaned = f.clean()
    return cleaned


def set_log_level(debug):
    log_name = logging.getLogger(LOGGER)
    log_level = "INFO"
    log_format = '%(levelname)s: %(message)s'
    if debug:
        log_level = "DEBUG"
    coloredlogs.install(level=log_level, fmt=log_format)


def read_file(filename):
    try:
        with open(filename, "r") as fh:
            return fh.read()
    except IOError as e:
        logging.error("could not read file '{}': {}".format(
            filename, e.strerror))
        sys.exit(EXIT_NOTFOUND)

import click
import json

from constant import VERSION, LOGGER
from cleaner import DeforestCleaner

@click.command()
@click.argument("infile")
@click.option("--outfile","-o", help="specify output file, default is ./<title>-<version>.<format>")
@click.option("--format","-f", default="yaml", show_default=True, type=click.Choice(["yaml","json"]), help="output format")
@click.option("--indent", "-i", default=4,type=int, help="if output format is json, specify indentation")
@click.version_option(None)
def main(infile,outfile,format,indent):
    with open(infile, "r") as fh:
        d = fh.read()

    cleaner = DeforestCleaner(d)
    result = cleaner.convert()

    if outfile:
        filename = outfile
    else:
        filename = "{}.{}".format(cleaner.get_title_and_version(),"json" if format == "json" else "yaml")

    with open(filename,"w+") as fh:
        if format == "json":
            fh.write(json.dumps(cleaner.get_raw(), indent=indent))
        else:
            fh.write(result)

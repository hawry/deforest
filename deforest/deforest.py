import click
import json

from constant import VERSION, LOGGER
from cleaner import DeforestCleaner
from solution import Solution

@click.command()
@click.argument("infile")
@click.option("--outfile","-o", help="specify output file, default is ./<title>-<version>.<format>, ignored if input is a CloudFormation template and the template contains more than one ApiGateway resource)")
@click.option("--format","-f", default="yaml", show_default=True, type=click.Choice(["yaml","json"]), help="output format")
@click.option("--indent", "-i", default=4,type=int, help="if output format is json, specify indentation")
@click.version_option(VERSION)
def main(infile,outfile,format,indent):
    with open(infile, "r") as fh:
        d = fh.read()

    cleaner = Solution(d).cleaner()
    result = cleaner.convert()

    filename = None
    if outfile and len(result) < 2:
        filename = outfile
    else:
        print("output will be in {} files, ignoring --outfile flag setting".format(len(result)))

    for i,r in enumerate(result):
        tfile = filename
        if filename is None:
            tfile = "{}.{}".format(cleaner.get_title_and_version_all(i),"json" if format == "json" else "yaml")

        with open(tfile,"w+") as fh:
            if format == "json":
                fh.write(json.dumps(cleaner.get_raw_all(i), indent=indent))
            else:
                fh.write(r)

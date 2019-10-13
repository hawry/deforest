# deforest

Remove all `x-amazon`-tags from your Open API 3 or Swagger 2 specification. Useful if you are using Cloudformation to specify your API Gateways, and want to provide your consumers with the same specification but not wanting to disclose your internal Amazon integrations.

# Installation

`pip install --user deforest`

## Features

- Clean keys starting with the string `x-amazon`
- Handles JSON and YAML input
- Handles JSON and YAML output (defaults to YAML)
- Support for AWS CloudFormation templates

# Usage

```
Usage: deforest [OPTIONS] INFILE

Options:
  -o, --outfile TEXT        specify output file, default is
                            ./<title>-<version>.<format>, ignored if input is
                            a CloudFormation template and the template
                            contains more than one ApiGateway resource)
  -f, --format [yaml|json]  output format  [default: yaml]
  -i, --indent INTEGER      if output format is json, specify indentation
  --version                 Show the version and exit.
  --help                    Show this message and exit.
```

## CloudFormation templates

Version 0.1.1 and later supports CloudFormation templates as input. If more than one API Gateway is part of the template, the `--outfile` flag will be ignored.

# Limitations

The output file looses its order of the keys in the file, which shouldn't affect you if you're using a converter to create a graphical documentation/specification - but can be confusing if you have a specific internal order you wish to keep.

# Contribute

If you wish to see a specific feature, please create an issue in the issue tracker - and if you want to help develop deforest, you're free to create a pull request as well. All submitted code will be subject to the licensing specified in the LICENSE file.

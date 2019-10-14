# deforest

[![PyPI version](https://badge.fury.io/py/deforest.svg)](https://badge.fury.io/py/deforest) [![Build Status](https://travis-ci.com/hawry/deforest.svg?branch=master)](https://travis-ci.com/hawry/deforest)

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
  -d, --debug               if enabled, show debug logs
  --no-ignore               if set, deforest will export paths marked as
                            ignored
  --version                 Show the version and exit.
  --help                    Show this message and exit.
```

## CloudFormation templates

Version 0.1.1 and later supports CloudFormation templates as input. If more than one API Gateway is part of the template, the `--outfile` flag will be ignored.

## Hide paths

Version 0.2.0 introduced support for deforest to ignore certain paths. If you specify `x-deforest-ignore: true` anywhere in your specification, deforest will not extract its _parent_ node to the end results. Example:

```yaml
paths:
  "/validation":
    post:
      responses:
        "200":
          schema:
            type: array
            items:
              "$ref": "#/definitions/Error"
          headers:
            test-method-response-header:
              type: string
    get:
      x-deforest-ignore: true
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
```

will result in

```yaml
paths:
  /validation:
    post:
      responses:
        "200":
          headers:
            test-method-response-header:
              type: string
          schema:
            items:
              $ref: "#/definitions/Error"
            type: array
```

If we'd written this:

```yaml
paths:
  "/validation":
    x-deforest-ignore: true
    post:
      responses:
        "200":
          schema:
            type: array
            items:
              "$ref": "#/definitions/Error"
          headers:
            test-method-response-header:
              type: string
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
```

we'd get an empty result since the _parent_ node is removed:

```yaml
paths: {}
```

If `x-deforest-ignore: false`, or missing, the node will be extracted as usual. If the runtime flag `--no-ignore` is set, the nodes will be extracted as usual as well.

# Limitations

The output file looses its order of the keys in the file, which shouldn't affect you if you're using a converter to create a graphical documentation/specification - but can be confusing if you have a specific internal order you wish to keep.

# Contribute

If you wish to see a specific feature, please create an issue in the issue tracker - and if you want to help develop deforest, you're free to create a pull request as well. All submitted code will be subject to the licensing specified in the LICENSE file.

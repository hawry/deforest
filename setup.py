import setuptools
import re
import os
from deforest.constant import VERSION

with open("README.md","r") as fh:
    long_desc = fh.read()

setuptools.setup(
    name="deforest",
    version=VERSION,
    author="hawry",
    entry_points = {
        "console_scripts": ["deforest=deforest.deforest:main"]
    },
    author_email="hawry@hawry.net",
    description="Remove all x-amazon tags from your OAS3 specification",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/hawry/deforester",
    packages=setuptools.find_packages(),
    install_requires=[
        "pyyaml==5.1.1",
        "click==6.7"
    ],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 3 - Alpha"
    ]
)

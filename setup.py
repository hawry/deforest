import setuptools
import re
import os

with open("README.md", "r") as fh:
    long_desc = fh.read()

setuptools.setup(
    name="deforest",
    version="0.4.0",
    author="hawry",
    entry_points={
        "console_scripts": ["deforest=deforest.deforest:main"]
    },
    author_email="hawry@hawry.net",
    description="Remove all x-amazon tags from your OAS3 specification",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/hawry/deforest",
    packages=setuptools.find_packages(),
    install_requires=[
        "pyyaml==5.4",
        "click==7.1.1",
        "coloredlogs==10.0"
    ],
    tests_require=[
        "parameterized",
        "pytest",
        "pytest-cov",
        "coverage"
    ],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 3 - Alpha"
    ]
)

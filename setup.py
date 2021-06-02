"""
Package setup.
"""
import configparser
import os
import site
import sys

from setuptools import find_packages, setup

site.ENABLE_USER_SITE = "--user" in sys.argv[1:]

VERSION = os.environ.get("VERSION", "0.9.1")
HERE = os.path.abspath(os.path.dirname(__file__))

config = configparser.ConfigParser()
config.read(os.path.join(HERE, "Pipfile"))
INSTALL_REQUIRES = [pkg.strip('"') for pkg in config["packages"].keys()]


def long_description() -> str:
    """
    Get the long description from the readme.
    """
    try:
        with open("README.md") as readme_file:
            return readme_file.read()
    except FileNotFoundError:
        return ""


setup(
    name="jsonschema-gentypes",
    version=VERSION,
    description="Tool to generate Python types based on TypedDict from a JSON Schema",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development :: Code Generators",
        "Typing :: Typed",
    ],
    keywords="jsonschema types",
    author="Camptocamp",
    author_email="info@camptocamp.com",
    url="https://github.com/camptocamp/jsonschema-gentypes",
    packages=find_packages(exclude=["tests", "docs"]),
    install_requires=INSTALL_REQUIRES,
    entry_points={
        "console_scripts": [
            "jsonschema-gentypes = jsonschema_gentypes.cli:main",
        ]
    },
    package_data={"jsonschema_gentypes": ["py.typed"]},
)

import configparser
import os

from setuptools import find_packages, setup

VERSION = os.environ.get("VERSION", "1.0.0")
HERE = os.path.abspath(os.path.dirname(__file__))

config = configparser.ConfigParser()
config.read(os.path.join(HERE, "Pipfile"))
INSTALL_REQUIRES = list(config["packages"].keys())


def long_description() -> str:
    try:
        with open("README.md") as readme_file:
            return readme_file.read()
    except FileNotFoundError:
        return ""


setup(
    name="project_name",
    version=VERSION,
    description="Common utilities for Camptocamp CI",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    keywords="ci",
    author="Camptocamp",
    author_email="info@camptocamp.com",
    url="https://github.com/camptocamp/c2cciutils",
    license="FreeBSD",
    packages=find_packages(exclude=["tests", "docs"]),
    install_requires=INSTALL_REQUIRES,
)

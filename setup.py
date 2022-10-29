# -*- coding: utf-8 -*-
import os
from distutils.core import setup

from setuptools import find_packages

setup(
    name="tdm-2022",
    version="1.0.0",
    install_requires=["mypy", "pre-commit"],
    extras_require={
        "arangodb": ["python-arango"],
        "janusgraph": [],
        "cosmodb": [],
    },
)

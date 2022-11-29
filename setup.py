# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name="tdm-2022",
    version="1.0.0",
    install_requires=["mypy", "pre-commit", "pandas", "python-decouple"],
    extras_require={
        "arangodb": ["python-arango"],
        "janusgraph": ["gremlinpython"],
        "cosmodb": [],
    },
)

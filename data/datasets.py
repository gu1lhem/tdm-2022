# -*- coding: utf-8 -*-
"""
Module that will create many datasets from the original one. The idea is to obtain different sized datasets
"""

import pandas as pd
from datasets import clear_data, get_data
from decouple import config

path = config("PATH_TO_DATA")
data = clear_data(get_data(path))

# Create a dataset with only the communes of the 1st department
data_1 = data[data["Code du departement"] == 1]

# Create a dataset with only the communes of the 1st to 20th department
data_20 = data[data["Code du departement"] <= 20]

# Create a dataset with only the communes of the 1st to 50th department
data_50 = data[data["Code du departement"] <= 50]

# Create a dataset with only the communes of the 1st to 100th department
data_100 = data[data["Code du departement"] <= 100]

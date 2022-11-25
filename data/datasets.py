# -*- coding: utf-8 -*-
"""
Module that will create many datasets from the original one. The idea is to obtain different sized datasets
"""

import pandas as pd
from decouple import config

from data.data_treatment import clear_data, get_data

path = config("PATH_TO_DATA")
data = clear_data(get_data(path))  # 35719 rows x 29 columns

# Create a dataset with only the communes of the 1st department
data_1 = data[data["Code du departement"] == "1"]  # 408 rows x 29 columns

# Create a dataset with only the communes of the 1st to 20th department
data_20 = data[data["Code du departement"] <= "20"]  # 4693 rows x 29 columns

# Create a dataset with only the communes of the 1st to 50th department
data_50 = data[data["Code du departement"] <= "45"]  # 15509 rows x 29 columns

# Create a dataset with only the communes of the 1st to 100th department
data_80 = data[data["Code du departement"] <= "75"]  # 28843 rows x 29 columns

# -*- coding: utf-8 -*-
"""
Module that will threat the data so that it can be used.

Data is like :
Code.du.departement	Libelle.du.departement	Code.de.la.commune	Libelle.de.la.commune	Inscrits	Abstentions	%Abs.Ins	Votants	%Vot.Ins	Blancs	%Blancs.Ins	%Blancs.Vot	Nuls	%Nuls.Ins	%Nuls.Vot	Exprimes	%Exp.Ins	%Exp.Vot	DUPONT-AIGNAN_Nicolas	LE PEN_Marine	MACRON_Emmanuel	HAMON_Benoit	ARTHAUD_Nathalie	POUTOU_Philippe	CHEMINADE_Jacques	LASSALLE_Jean	MELENCHON_Jean-Luc	ASSELINEAU_Francois	FILLON_Francois
1	Ain	1	L'Abergement-Clémenciat	598	92	15.38	506	84.62	2	0.33	0.4	9	1.51	1.78	495	82.78	97.83	6.87	25.45	24.04	5.86	0.81	0.81	0.4	0.4	11.92	1.21	22.22
1	Ain	2	L'Abergement-de-Varey	209	25	11.96	184	88.04	6	2.87	3.26	2	0.96	1.09	176	84.21	95.65	3.41	27.27	21.02	7.39	1.14	1.14	0	0	18.75	0.57	19.32
1	Ain	4	Ambérieu-en-Bugey	8586	1962	22.85	6624	77.15	114	1.33	1.72	58	0.68	0.88	6452	75.15	97.4	5.36	25.84	20.64	5.33	0.62	1.41	0.08	0.93	21.88	1.1	16.8
1	Ain	5	Ambérieux-en-Dombes	1172	215	18.34	957	81.66	21	1.79	2.19	3	0.26	0.31	933	79.61	97.49	4.82	32.8	20.47	3.97	0.54	1.07	0	0.64	13.5	1.07	21.11

This is a CSV file, with the first line being the headers.
"""

import pandas as pd
from decouple import config

path = config("PATH_TO_DATA")


def get_data(path: str, separator: str = ";") -> pd.DataFrame:
    """
    Function that will return the data from the CSV file.

    Args:
        path (str): Path to the CSV file.
        separator (str): Separator used in the CSV file.

    Returns:
        pd.DataFrame: Dataframe containing the data.

    Requires:
        pandas
    """
    if path.endswith(".csv"):
        try:
            return pd.read_csv(path, sep=separator)
        except UnicodeDecodeError:
            return pd.read_csv(path, sep=separator, encoding="latin-1")
    else:
        raise ValueError("The path given is not a CSV file.")


def clear_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Function that will clear the data from the CSV file.

    Args:
        data (pd.DataFrame): Dataframe containing the data.

    Returns:
        pd.DataFrame: Dataframe containing the data.

    Requires:
        pandas
    """

    # We replace the _ and . by a space
    data.columns = [
        header.replace("_", " ").replace(".", " ") for header in data.columns
    ]

    return data


print(clear_data(get_data(path)))

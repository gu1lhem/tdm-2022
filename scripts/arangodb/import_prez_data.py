# -*- coding: utf-8 -*-
from connection import client
from datasets import data, data_1, data_20, data_50, data_100
from decouple import config

path = config("PATH_TO_DATA")
username = config("ARANGO_USERNAME")
password = config("ARANGO_PASSWORD")
database = config("ARANGO_DB_NAME")

# Connect to "_system" database as root user.
sys_db = client.db("_system", username=username, password=password)

# Create a new database named "tdm-2022".
if not sys_db.has_database(database):
    sys_db.create_database(database)

# Connect to "tdm-2022" database as root user.
db = client.db(database, username=username, password=password)

# Create a new graph named "prez-2017".
graph = db.create_graph("prez-2017")

# Create vertex collections for the graph.
candidats = graph.create_vertex_collection("candidats")
communes = graph.create_vertex_collection("communes")

# Create an edge definition (relation) for the graph.
edges = graph.create_edge_definition(
    edge_collection="elit",
    from_vertex_collections=["communes"],
    to_vertex_collections=["candidats"],
)


candidats.insert({"_key": "EM", "full_name": "Emmanuel Macron"})
candidats.insert({"_key": "MLP", "full_name": "Marine Le Pen"})
candidats.insert({"_key": "NDA", "full_name": "Nicolas Dupont-Aignan"})
candidats.insert({"_key": "JLM", "full_name": "Jean-Luc Mélenchon"})
candidats.insert({"_key": "FF", "full_name": "Francois Fillon"})
candidats.insert({"_key": "BH", "full_name": "Benoît Hamon"})
candidats.insert({"_key": "NA", "full_name": "Nathalie Arthaud"})
candidats.insert({"_key": "PP", "full_name": "Philippe Poutou"})
candidats.insert({"_key": "FA", "full_name": "Francois Asselineau"})
candidats.insert({"_key": "JC", "full_name": "Jacques Cheminade"})
candidats.insert({"_key": "JL", "full_name": "Jean Lassalle"})

for index, row in data.iterrows():
    commune_key = f"D{row['Code du departement']}C{row['Code de la commune']}"
    communes.insert(
        {
            "_key": commune_key,
            "libelle_commune": row["Libelle de la commune"],
            "code_commune": row["Code de la commune"],
            "code_departement": row["Code du departement"],
            "libelle_departement": row["Libelle du departement"],
            "inscrits": row["Inscrits"],
            "abstentions": row["Abstentions"],
            "%Abs Ins": row["%Abs Ins"],
            "votants": row["Votants"],
            "%Vot Ins": row["%Vot Ins"],
            "blancs": row["Blancs"],
            "%Blancs Ins": row["%Blancs Ins"],
            "%Blancs Vot": row["%Blancs Vot"],
            "nuls": row["Nuls"],
            "%Nuls Ins": row["%Nuls Ins"],
            "%Nuls Vot": row["%Nuls Vot"],
            "exprimes": row["Exprimes"],
            "%Exp Ins": row["%Exp Ins"],
            "%Exp Vot": row["%Exp Vot"],
        }
    )
    edges.insert(
        {
            "_from": f"communes/{commune_key}",
            "_to": "candidats/EM",
            "score": row["MACRON Emmanuel"],
        }
    )
    edges.insert(
        {
            "_from": f"communes/{commune_key}",
            "_to": "candidats/MLP",
            "score": row["LE PEN Marine"],
        }
    )
    edges.insert(
        {
            "_from": f"communes/{commune_key}",
            "_to": "candidats/NDA",
            "score": row["DUPONT-AIGNAN Nicolas"],
        }
    )
    edges.insert(
        {
            "_from": f"communes/{commune_key}",
            "_to": "candidats/JLM",
            "score": row["MELENCHON Jean-Luc"],
        }
    )
    edges.insert(
        {
            "_from": f"communes/{commune_key}",
            "_to": "candidats/FF",
            "score": row["FILLON Francois"],
        }
    )
    edges.insert(
        {
            "_from": f"communes/{commune_key}",
            "_to": "candidats/BH",
            "score": row["HAMON Benoit"],
        }
    )
    edges.insert(
        {
            "_from": f"communes/{commune_key}",
            "_to": "candidats/NA",
            "score": row["ARTHAUD Nathalie"],
        }
    )
    edges.insert(
        {
            "_from": f"communes/{commune_key}",
            "_to": "candidats/PP",
            "score": row["POUTOU Philippe"],
        }
    )
    edges.insert(
        {
            "_from": f"communes/{commune_key}",
            "_to": "candidats/FA",
            "score": row["ASSELINEAU Francois"],
        }
    )
    edges.insert(
        {
            "_from": f"communes/{commune_key}",
            "_to": "candidats/JC",
            "score": row["CHEMINADE Jacques"],
        }
    )
    edges.insert(
        {
            "_from": f"communes/{commune_key}",
            "_to": "candidats/JL",
            "score": row["LASSALLE Jean"],
        }
    )

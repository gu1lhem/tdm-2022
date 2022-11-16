# -*- coding: utf-8 -*-
from connection import client

# Connect to "_system" database as root user.
sys_db = client.db("_system", username="root", password="Password")

# Create a new database named "prez2017_1".
sys_db.create_database("prez2017_1")

# Connect to "prez2017_1" database as root user.
db = client.db("prez2017_1", username="root", password="Password")

# Create a new collection named "communes".
communes = db.create_collection("communes")

# Add a hash index to the collection.
communes.add_hash_index(fields=["libelle"], unique=True)

communes.insert({"name": "jane", "age": 39})
communes.insert({"name": "josh", "age": 18})
communes.insert({"name": "judy", "age": 21})

# Create a new collection named "departements".
departements = db.create_collection("departements")

# Add a hash index to the collection.
departements.add_hash_index(fields=["libelle"], unique=True)


# Create a new collection named "candidats".
candidats = db.create_collection("candidats")

candidats.insert({"name": "Le Pen", "firstname": "Marine"})
candidats.insert({"name": "Dupont-Aignan", "firstname": "Nicolas"})
candidats.insert({"name": "Macron", "firstname": "Emmanuel"})
candidats.insert({"name": "Mélenchon", "firstname": "Jean-Luc"})
candidats.insert({"name": "Hamon", "firstname": "Benoit"})
candidats.insert({"name": "Arthaud", "firstname": "Nathalie"})
candidats.insert({"name": "Poutou", "firstname": "Philippe"})
candidats.insert({"name": "Cheminade", "firstname": "Jacques"})
candidats.insert({"name": "Lassalle", "firstname": "Jean"})
candidats.insert({"name": "Asselineau", "firstname": "Francois"})
candidats.insert({"name": "Fillon", "firstname": "Francois"})

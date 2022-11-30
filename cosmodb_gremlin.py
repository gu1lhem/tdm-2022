# -*- coding: utf-8 -*-
# This script will connect to the CosmoDB account, that is a ThinkerPop instance
# and will create a new database and a new collection.


import asyncio  # asyncio.run() is used to run the main() function.
import sys  # sys.exit() is used to exit the script with a specific exit code.
import traceback  # traceback.print_exc() is used to print the stack trace of the exception.
from time import time

from decouple import \
    config  # decouple is used to read the environment variables from the .env file.
from gremlin_python.driver import (  # This is the endpoint of the Gremlin server.
    client, protocol, serializer)
from gremlin_python.driver.protocol import \
    GremlinServerError  # GremlinServerError is raised when the server returns an error.

from data.data_treatment import clear_data, get_data

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # This is required on Windows to avoid the following error:
    # RuntimeError: There is no current event loop in thread 'Thread-1'.


path = config("PATH_TO_DATA")
COSMODB_ENDPOINT = config("COSMODB_ENDPOINT")
COSMODB_DATABASE = config("COSMODB_DATABASE")
COSMODB_GRAPH = config("COSMODB_GRAPH")
COSMODB_PASSWORD = config("COSMODB_PASSWORD")

data = clear_data(get_data(path))

print(data)

"""
data is like :
[35719 rows x 29 columns]
Code.du.departement 	Libelle.du.departement 	Code.de.la.commune 	Libelle.de.la.commune 	Inscrits 	Abstentions 	%Abs.Ins 	Votants 	%Vot.Ins 	Blancs 	%Blancs.Ins 	%Blancs.Vot 	Nuls 	%Nuls.Ins 	%Nuls.Vot 	Exprimes 	%Exp.Ins 	%Exp.Vot 	DUPONT-AIGNAN_Nicolas 	LE PEN_Marine 	MACRON_Emmanuel 	HAMON_Benoit 	ARTHAUD_Nathalie 	POUTOU_Philippe 	CHEMINADE_Jacques 	LASSALLE_Jean 	MELENCHON_Jean-Luc 	ASSELINEAU_Francois 	FILLON_Francois
1 	Ain 	1 	L’Abergement-Clémenciat 	598 	92 	15.38 	506 	84.62 	2 	0.33 	0.4 	9 	1.51 	1.78 	495 	82.78 	97.83 	6.87 	25.45 	24.04 	5.86 	0.81 	0.81 	0.4 	0.4 	11.92 	1.21 	22.22
1 	Ain 	2 	L’Abergement-de-Varey 	209 	25 	11.96 	184 	88.04 	6 	2.87 	3.26 	2 	0.96 	1.09 	176 	84.21 	95.65 	3.41 	27.27 	21.02 	7.39 	1.14 	1.14 	0 	0 	18.75 	0.57 	19.32
1 	Ain 	4 	Ambérieu-en-Bugey 	8586 	1962 	22.85 	6624 	77.15 	114 	1.33 	1.72 	58 	0.68 	0.88 	6452 	75.15 	97.4 	5.36 	25.84 	20.64 	5.33 	0.62 	1.41 	0.08 	0.93 	21.88 	1.1 	16.8
"""

candidats_dict = {
    "EM": "MACRON Emmanuel",
    "MLP": "LE PEN Marine",
    "NDA": "DUPONT-AIGNAN Nicolas",
    "JLM": "MELENCHON Jean-Luc",
    "FF": "FILLON Francois",
    "BH": "HAMON Benoit",
    "NA": "ARTHAUD Nathalie",
    "PP": "POUTOU Philippe",
    "FA": "ASSELINEAU Francois",
    "JC": "CHEMINADE Jacques",
    "JL": "LASSALLE Jean",
}

_gremlin_cleanup_graph = "g.V().drop()"


def cleanup_graph(client):
    print("\n> {0}".format(_gremlin_cleanup_graph))
    callback = client.submitAsync(_gremlin_cleanup_graph)
    if callback.result() is not None:
        callback.result().all().result()
    print("\n")
    print_status_attributes(callback.result())
    print("\n")


def print_status_attributes(result):
    # This logs the status attributes returned for successful requests.
    # See list of available response status attributes (headers) that Gremlin API can return:
    #     https://docs.microsoft.com/en-us/azure/cosmos-db/gremlin-headers#headers
    #
    # These responses includes total request units charged and total server latency time.
    #
    # IMPORTANT: Make sure to consume ALL results returend by cliient tothe final status attributes
    # for a request. Gremlin result are stream as a sequence of partial response messages
    # where the last response contents the complete status attributes set.
    #
    # This can be
    print("\tResponse status_attributes:\n\t{0}".format(result.status_attributes))


try:
    client = client.Client(
        f"wss://{COSMODB_ENDPOINT}.gremlin.cosmos.azure.com:443/",
        "g",
        username=f"/dbs/{COSMODB_DATABASE}/colls/{COSMODB_GRAPH}",
        password=f"{COSMODB_PASSWORD}",
        message_serializer=serializer.GraphSONSerializersV2d0(),
    )

    print("Welcome to Azure Cosmos DB + Gremlin on Python!")

    # Drop the entire Graph
    inp = input(
        "We're about to drop whatever graph is on the server. Press y to continue, any other key to abort."
    )
    if inp == "y":
        cleanup_graph(client)
except GremlinServerError as e:
    print("Code: {0}, Attributes: {1}".format(e.status_code, e.status_attributes))

    # GremlinServerError.status_code returns the Gremlin protocol status code
    # These are broad status codes which can cover various scenaios, so for more specific
    # error handling we recommend using GremlinServerError.status_attributes['x-ms-status-code']
    #
    # Below shows how to capture the Cosmos DB specific status code and perform specific error handling.
    # See detailed set status codes than can be returned here: https://docs.microsoft.com/en-us/azure/cosmos-db/gremlin-headers#status-codes
    #
    # See also list of available response status attributes that Gremlin API can return:
    #     https://docs.microsoft.com/en-us/azure/cosmos-db/gremlin-headers#headers
    cosmos_status_code = e.status_attributes["x-ms-status-code"]
    if cosmos_status_code == 409:
        print("Conflict error!")
    elif cosmos_status_code == 412:
        print("Precondition error!")
    elif cosmos_status_code == 429:
        print("Throttling error!")
    elif cosmos_status_code == 1009:
        print("Request timeout error!")
    else:
        print("Default error handling")

    traceback.print_exc(file=sys.stdout)
    sys.exit(1)


def create_insert_vertices_query(data):
    """
    Create the query to insert the vertices in the graph from the `data` DataFrame.
    """
    # We will create two collections : 'candidats' and 'communes'.
    # The 'candidats' collection will contain the candidats.
    # The 'communes' collection will contain the communes.

    # We will create a list of queries to insert the vertices.
    queries = []

    # We will create a query to insert the candidats with the dict
    for candidat in candidats_dict:
        query = "g.addV('candidat').property('pk', '{0}').property('full_name', '{1}')".format(
            candidat, candidats_dict[candidat]
        )
        queries.append(query)

    for index, row in data.iterrows():
        commune_key = f"D{row['Code du departement']}C{row['Code de la commune']}"
        libelle_commune = (
            row["Libelle de la commune"].replace("'", r"\'").replace('"', "")
        )
        libelle_departement = (
            row["Libelle du departement"].replace("'", r"\'").replace('"', ""),
        )
        libelle_departement = libelle_departement[0]
        query = f"g.addV('commune').property('pk', '{commune_key}')"
        query += f".property('libelle_commune', '{libelle_commune}')"
        query += f".property('code_commune', '{row['Code de la commune']}')"
        query += f".property('code_departement', '{row['Code du departement']}')"
        query += f".property('libelle_departement', '{libelle_departement}')"
        query += f".property('inscrits', {row['Inscrits']})"
        query += f".property('abstentions', {row['Abstentions']})"
        query += f".property('pourcentage_abstentions', {row['%Abs Ins']}f)"
        query += f".property('votants', {row['Votants']})"
        query += f".property('pourcentage_votants', {row['%Vot Ins']}f)"
        query += f".property('blancs', {row['Blancs']})"
        query += f".property('pourcentage_blancs', {row['%Blancs Ins']}f)"
        query += f".property('pourcentage_blancs_sur_votants', {row['%Blancs Vot']}f)"
        query += f".property('nuls', {row['Nuls']})"
        query += f".property('pourcentage_nuls', {row['%Nuls Ins']}f)"
        query += f".property('pourcentage_nuls_sur_votants', {row['%Nuls Vot']}f)"
        query += f".property('exprimes', {row['Exprimes']})"
        query += f".property('pourcentage_exprimes', {row['%Exp Ins']}f)"
        query += f".property('pourcentage_exprimes_sur_votants', {row['%Exp Vot']}f)"

        queries.append(query)

    return queries


def insert_vertices(client, _gremlin_insert_vertices):
    for query in _gremlin_insert_vertices:
        print("\n> {0}\n".format(query))
        callback = client.submitAsync(query)
        if callback.result() is not None:
            print(
                "\tInserted this vertex:\n\t{0}".format(
                    callback.result().all().result()
                )
            )
        else:
            print("Something went wrong with this query: {0}".format(query))
        print("\n")
        print_status_attributes(callback.result())
        print("\n")

    print("\n")


# count execution time
start_time = time.time()

try:
    inp = input("We're about to insert the vertices. Press y to continue...")
    if inp == "y":
        _gremlin_insert_vertices = create_insert_vertices_query(data)
        insert_vertices(client, _gremlin_insert_vertices)

        end_time = time.time()

        print("Execution time: {0} seconds".format(end_time - start_time))

except GremlinServerError as e:
    print("Code: {0}, Attributes: {1}".format(e.status_code, e.status_attributes))

    # GremlinServerError.status_code returns the Gremlin protocol status code
    # These are broad status codes which can cover various scenaios, so for more specific
    # error handling we recommend using GremlinServerError.status_attributes['x-ms-status-code']
    #
    # Below shows how to capture the Cosmos DB specific status code and perform specific error handling.
    # See detailed set status codes than can be returned here: https://docs.microsoft.com/en-us/azure/cosmos-db/gremlin-headers#status-codes
    #
    # See also list of available response status attributes that Gremlin API can return:
    #     https://docs.microsoft.com/en-us/azure/cosmos-db/gremlin-headers#headers
    cosmos_status_code = e.status_attributes["x-ms-status-code"]
    if cosmos_status_code == 409:
        print("Conflict error!")
    elif cosmos_status_code == 412:
        print("Precondition error!")
    elif cosmos_status_code == 429:
        print("Throttling error!")
    elif cosmos_status_code == 1009:
        print("Request timeout error!")
    else:
        print("Default error handling")

    traceback.print_exc(file=sys.stdout)
    sys.exit(1)


def create_insert_edges_query(data):
    """
    Create the query to insert the edges.
    """
    # The 'candidats' collection will be linked to the 'communes' collection with the 'score' edge.

    # We will create a list of queries to insert the edges.
    queries = []

    for index, row in data.iterrows():
        commune_key = f"D{row['Code du departement']}C{row['Code de la commune']}"

        # We will create a query to insert the edges with the dict
        for candidat in candidats_dict:
            query = f"g.V('{commune_key}').addE('score').to(g.V('{candidat}')).property('score', {row[candidats_dict[candidat]]}f).next()"
            queries.append(query)

    return queries


def insert_edges(client, _gremlin_insert_edges):
    for query in _gremlin_insert_edges:
        print("\n> {0}\n".format(query))
        callback = client.submitAsync(query)
        if callback.result() is not None:
            print(
                "\tInserted this edge:\n\t{0}\n".format(
                    callback.result().all().result()
                )
            )
        else:
            print("Something went wrong with this query:\n\t{0}".format(query))
        print_status_attributes(callback.result())
        print("\n")

    print("\n")


# count execution time
start_time = time.time()

try:
    inp = input("We're about to insert the edges. Press y to continue...")
    if inp == "y":
        _gremlin_insert_edges = create_insert_edges_query(data)
        insert_edges(client, _gremlin_insert_edges)

        end_time = time.time()
        print("Execution time: {0} seconds".format(end_time - start_time))

except GremlinServerError as e:
    print("Code: {0}, Attributes: {1}".format(e.status_code, e.status_attributes))

    # GremlinServerError.status_code returns the Gremlin protocol status code
    # These are broad status codes which can cover various scenaios, so for more specific
    # error handling we recommend using GremlinServerError.status_attributes['x-ms-status-code']
    #
    # Below shows how to capture the Cosmos DB specific status code and perform specific error handling.
    # See detailed set status codes than can be returned here: https://docs.microsoft.com/en-us/azure/cosmos-db/gremlin-headers#status-codes
    #
    # See also list of available response status attributes that Gremlin API can return:
    #     https://docs.microsoft.com/en-us/azure/cosmos-db/gremlin-headers#headers
    cosmos_status_code = e.status_attributes["x-ms-status-code"]
    if cosmos_status_code == 409:
        print("Conflict error!")
    elif cosmos_status_code == 412:
        print("Precondition error!")
    elif cosmos_status_code == 429:
        print("Throttling error!")
    elif cosmos_status_code == 1009:
        print("Request timeout error!")
    else:
        print("Default error handling")

    traceback.print_exc(file=sys.stdout)
    sys.exit(1)


"""
_gremlin_update_vertices = ["g.V('thomas').property('age', 45)"]

_gremlin_count_vertices = "g.V().count()"

_gremlin_traversals = {
    "Get all persons older than 40": "g.V().hasLabel('person').has('age', gt(40)).values('firstName', 'age')",
    "Get all persons and their first name": "g.V().hasLabel('person').values('firstName')",
    "Get all persons sorted by first name": "g.V().hasLabel('person').order().by('firstName', incr).values('firstName')",
    "Get all persons that Thomas knows": "g.V('thomas').out('knows').hasLabel('person').values('firstName')",
    "People known by those who Thomas knows": "g.V('thomas').out('knows').hasLabel('person').out('knows').hasLabel('person').values('firstName')",
    "Get the path from Thomas to Robin": "g.V('thomas').repeat(out()).until(has('pk', 'robin')).path().by('firstName')",
}

_gremlin_drop_operations = {
    "Drop Edge - Thomas no longer knows Mary": "g.V('thomas').outE('knows').where(inV().has('pk', 'mary')).drop()",
    "Drop Vertex - Drop Thomas": "g.V('thomas').drop()",
}
"""


def update_vertices(client):
    for query in _gremlin_update_vertices:
        print("\n> {0}\n".format(query))
        callback = client.submitAsync(query)
        if callback.result() is not None:
            print(
                "\tUpdated this vertex:\n\t{0}\n".format(
                    callback.result().all().result()
                )
            )
        else:
            print("Something went wrong with this query:\n\t{0}".format(query))

        print_status_attributes(callback.result())
        print("\n")

    print("\n")


def count_vertices(client):
    print("\n> {0}".format(_gremlin_count_vertices))
    callback = client.submitAsync(_gremlin_count_vertices)
    if callback.result() is not None:
        print("\tCount of vertices: {0}".format(callback.result().all().result()))
    else:
        print(
            "Something went wrong with this query: {0}".format(_gremlin_count_vertices)
        )

    print("\n")
    print_status_attributes(callback.result())
    print("\n")


def execute_traversals(client):
    for key in _gremlin_traversals:
        print("{0}:".format(key))
        print("> {0}\n".format(_gremlin_traversals[key]))
        callback = client.submitAsync(_gremlin_traversals[key])
        for result in callback.result():
            print("\t{0}".format(str(result)))

        print("\n")
        print_status_attributes(callback.result())
        print("\n")


def execute_drop_operations(client):
    for key in _gremlin_drop_operations:
        print("{0}:".format(key))
        print("\n> {0}".format(_gremlin_drop_operations[key]))
        callback = client.submitAsync(_gremlin_drop_operations[key])
        for result in callback.result():
            print(result)
        print_status_attributes(callback.result())
        print("\n")


def just_run(client, query):
    print("\n> {0}".format(query))
    callback = client.submitAsync(query)
    if callback.result() is not None:
        print("\t{0}".format(callback.result().all().result()))
    else:
        print("Something went wrong with this query: {0}".format(query))

    print("\n")
    print_status_attributes(callback.result())
    print("\n")


try:
    input("We are about to get data from the graph. Press any key to continue...")
    # Now, we will execute different Gremlin queries:

    # 1- the 10 Communes where there are the most Inscrits

    _gremlin_query_1 = "g.V().hasLabel('Commune').order().by('Inscrits', decr).limit(10).values('Nom', 'Inscrits')"
    just_run(client, _gremlin_query_1)

    # 2- The score of Emmanuel Maccron in Paris

    _gremlin_query_2 = "g.V().hasLabel('Commune').has('Nom', 'Paris').outE('Score').inV().has('Nom', 'Emmanuel Macron').values('Score')"
    just_run(client, _gremlin_query_2)

    # 3- For each Candidat, the city where he has the highest score

    _gremlin_query_3 = "g.V().hasLabel('Candidat').as('candidat').outE('Score').inV().as('commune').order().by('Score', decr).dedup('candidat').select('candidat', 'commune').by('Nom').by('Nom')"
    just_run(client, _gremlin_query_3)

    # 4- Results for the Commune where the Abstention is > 50%

    _gremlin_query_4 = "g.V().hasLabel('Commune').has('Abstention', gt(50)).values('Nom', 'Abstention')"
    just_run(client, _gremlin_query_4)

    # 5- The winner for each `Libelle du departement` (Département)
    # We will use the `fold` step to collect all the scores for each Candidat

    _gremlin_query_5 = "g.V().hasLabel('Departement').as('departement').outE('Score').inV().as('candidat').order().by('Score', decr).dedup('departement').select('departement', 'candidat').by('Libelle').by('Nom')"
    just_run(client, _gremlin_query_5)

    # 6- For each Candidat, transfor the percentage by the number of Inscrit, and order by the number of Exprimés

    _gremlin_query_6 = "g.V().hasLabel('Candidat').as('candidat').outE('Score').inV().as('commune').select('candidat', 'commune').by('Nom').by('Inscrits', 'Exprimes', 'Abstention').by('Score').map{it.get().value.get('commune').value.get('Inscrits') * it.get().value.get('candidat').value.get('Score') / 100}.order().by(local, decr).dedup('candidat').select('candidat', 'commune').by('Nom').by('Nom')"
    just_run(client, _gremlin_query_6)

except GremlinServerError as e:
    print("Code: {0}, Attributes: {1}".format(e.status_code, e.status_attributes))

    # GremlinServerError.status_code returns the Gremlin protocol status code
    # These are broad status codes which can cover various scenaios, so for more specific
    # error handling we recommend using GremlinServerError.status_attributes['x-ms-status-code']
    #
    # Below shows how to capture the Cosmos DB specific status code and perform specific error handling.
    # See detailed set status codes than can be returned here: https://docs.microsoft.com/en-us/azure/cosmos-db/gremlin-headers#status-codes
    #
    # See also list of available response status attributes that Gremlin API can return:
    #     https://docs.microsoft.com/en-us/azure/cosmos-db/gremlin-headers#headers
    cosmos_status_code = e.status_attributes["x-ms-status-code"]
    if cosmos_status_code == 409:
        print("Conflict error!")
    elif cosmos_status_code == 412:
        print("Precondition error!")
    elif cosmos_status_code == 429:
        print("Throttling error!")
    elif cosmos_status_code == 1009:
        print("Request timeout error!")
    else:
        print("Default error handling")

    traceback.print_exc(file=sys.stdout)
    sys.exit(1)


try:

    """
    # Update a vertex
    input(
        "Ah, sorry. I made a mistake. Let's change the age of this vertex. Press any key to continue..."
    )
    update_vertices(client)

    # Count all vertices
    input("Okay. Let's count how many vertices we have. Press any key to continue...")
    count_vertices(client)

    # Execute traversals and get results
    input("Cool! Let's run some traversals on our graph. Press any key to continue...")
    execute_traversals(client)

    # Drop a few vertices and edges
    input(
        "So, life happens and now we will make some changes to the graph. Press any key to continue..."
    )
    execute_drop_operations(client)

    # Count all vertices again
    input("How many vertices do we have left? Press any key to continue...")
    count_vertices(client)


    # We will make the requests we decided to do:

    # Get the candidate with the most votes in each commune
    print("Get the candidate with the most votes in each commune")

    query = "g.V().hasLabel('commune').as('commune').out('has').as('candidate').group().by('commune').by(out('has').order().by('votes', decr).limit(1).values('name')).select('commune', 'candidate')"
    callback = client.submitAsync(query)
    for result in callback.result():
        print("\t{0}".format(str(result)))

    """


except GremlinServerError as e:
    print("Code: {0}, Attributes: {1}".format(e.status_code, e.status_attributes))

    # GremlinServerError.status_code returns the Gremlin protocol status code
    # These are broad status codes which can cover various scenaios, so for more specific
    # error handling we recommend using GremlinServerError.status_attributes['x-ms-status-code']
    #
    # Below shows how to capture the Cosmos DB specific status code and perform specific error handling.
    # See detailed set status codes than can be returned here: https://docs.microsoft.com/en-us/azure/cosmos-db/gremlin-headers#status-codes
    #
    # See also list of available response status attributes that Gremlin API can return:
    #     https://docs.microsoft.com/en-us/azure/cosmos-db/gremlin-headers#headers
    cosmos_status_code = e.status_attributes["x-ms-status-code"]
    if cosmos_status_code == 409:
        print("Conflict error!")
    elif cosmos_status_code == 412:
        print("Precondition error!")
    elif cosmos_status_code == 429:
        print("Throttling error!")
    elif cosmos_status_code == 1009:
        print("Request timeout error!")
    else:
        print("Default error handling")

    traceback.print_exc(file=sys.stdout)
    sys.exit(1)

print("\nAnd that's all! Sample complete")
input("Press Enter to continue...")

# -*- coding: utf-8 -*-
# This script will connect to the Janusgraph account, that is a ThinkerPop instance
# and will create a new database and a new collection.


import asyncio  # asyncio.run() is used to run the main() function.
import sys
import time
import traceback  # traceback.print_exc() is used to print the stack trace of the exception.

from decouple import \
    config  # decouple is used to read the environment variables from the .env file.
from gremlin_python.driver import (  # This is the endpoint of the Gremlin server.
    client, protocol, serializer)
from gremlin_python.driver.driver_remote_connection import \
    DriverRemoteConnection
from gremlin_python.driver.protocol import \
    GremlinServerError  # GremlinServerError is raised when the server returns an error.
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.graph_traversal import __
from gremlin_python.structure.graph import Graph

from data.data_treatment import clear_data, get_data

path = config("PATH_TO_DATA")
JANUSGRAPH_HOST = config("JANUSGRAPH_HOST")
JANUSGRAPH_PORT = config("JANUSGRAPH_PORT")
JANUSGRAPH_DB_NAME = config("JANUSGRAPH_DB_NAME")

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
        query = "g.addV('candidat').property('id', '{0}').property('full_name', '{1}')".format(
            candidat, candidats_dict[candidat]
        )
        queries.append(query)

    for index, row in data.iterrows():

        commune_key = f"D{row['Code du departement']}C{row['Code de la commune']}"
        query = "g.addV('commune').property('id', '{0}').property('libelle_commune', '{1}').property('code_commune', '{2}').property('code_departement', '{3}').property('libelle_departement', '{4}').property('inscrits', {5}).property('abstentions', {6}).property('pourcentage_abstentions', {7}f).property('votants', {8}).property('pourcentage_votants', {9}f).property('blancs', {10}).property('pourcentage_blancs', {11}f).property('pourcentage_blancs_sur_votants', {12}f).property('nuls', {13}).property('pourcentage_nuls', {14}f).property('pourcentage_nuls_sur_votants', {15}f).property('exprimes', {16}).property('pourcentage_exprimes', {17}f).property('pourcentage_exprimes_sur_votants', {18}f)".format(
            commune_key,
            row["Libelle de la commune"].replace("'", r"\'"),
            row["Code de la commune"],
            row["Code du departement"],
            row["Libelle du departement"].replace("'", r"\'"),
            row["Inscrits"],
            row["Abstentions"],
            row["%Abs Ins"],
            row["Votants"],
            row["%Vot Ins"],
            row["Blancs"],
            row["%Blancs Ins"],
            row["%Blancs Vot"],
            row["Nuls"],
            row["%Nuls Ins"],
            row["%Nuls Vot"],
            row["Exprimes"],
            row["%Exp Ins"],
            row["%Exp Vot"],
        )
        queries.append(query)

    return queries


_gremlin_insert_vertices = create_insert_vertices_query(data)


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
            query = f"g.V().has('id','{commune_key}').addE('Score').to(__.V().has('id','{candidat}')).property('score', {row[candidats_dict[candidat]]}f)"
            queries.append(query)

    return queries


_gremlin_insert_edges = create_insert_edges_query(data)


def insert_vertices(client):
    for query in _gremlin_insert_vertices:
        # print("\n> {0}\n".format(query))
        callback = client.submit_async(query)
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


if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # This is required on Windows to avoid the following error:
    # RuntimeError: There is no current event loop in thread 'Thread-1'.


_gremlin_cleanup_graph = "g.V().drop()"

"""
_gremlin_update_vertices = ["g.V('thomas').property('age', 45)"]

_gremlin_count_vertices = "g.V().count()"

_gremlin_traversals = {
    "Get all persons older than 40": "g.V().hasLabel('person').has('age', gt(40)).values('firstName', 'age')",
    "Get all persons and their first name": "g.V().hasLabel('person').values('firstName')",
    "Get all persons sorted by first name": "g.V().hasLabel('person').order().by('firstName', incr).values('firstName')",
    "Get all persons that Thomas knows": "g.V('thomas').out('knows').hasLabel('person').values('firstName')",
    "People known by those who Thomas knows": "g.V('thomas').out('knows').hasLabel('person').out('knows').hasLabel('person').values('firstName')",
    "Get the path from Thomas to Robin": "g.V('thomas').repeat(out()).until(has('id', 'robin')).path().by('firstName')",
}

_gremlin_drop_operations = {
    "Drop Edge - Thomas no longer knows Mary": "g.V('thomas').outE('knows').where(inV().has('id', 'mary')).drop()",
    "Drop Vertex - Drop Thomas": "g.V('thomas').drop()",
}
"""


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


def cleanup_graph(client):
    print("\n> {0}".format(_gremlin_cleanup_graph))
    callback = client.submit_async(_gremlin_cleanup_graph)
    if callback.result() is not None:
        callback.result().all().result()
    print("\n")
    print_status_attributes(callback.result())
    print("\n")


def insert_edges(client):
    for query in _gremlin_insert_edges:
        print("\n> {0}\n".format(query))
        callback = client.submitAsync(query)
        if callback.result() is not None:
            print("\tInserted this edge:")
        else:
            print("Something went wrong with this query:\n\t{0}".format(query))
        print_status_attributes(callback.result())
        print("\n")

    print("\n")


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


try:
    # The connection should be closed on shut down to close open connections with connection.close()
    client = client.Client(
        f"ws://{JANUSGRAPH_HOST}:{JANUSGRAPH_PORT}/{JANUSGRAPH_DB_NAME}", "g"
    )

    print("Welcome to Janusgraph + Gremlin on Python!")

    # Drop the entire Graph
    input(
        "We're about to drop whatever graph is on the server. Press any key to continue..."
    )
    # start_time = time.time()
    # cleanup_graph(client)
    # end_time = time.time()
    # print(f"Cleanup graph took {end_time - start_time} seconds")
    # Insert all vertices
    input("Let's insert some vertices into the graph. Press any key to continue...")
    # count execution time
    start_time = time.time()
    insert_vertices(client)
    end_time = time.time()
    print(
        "Execution time to insert vertices: {0} seconds".format(end_time - start_time)
    )

    # Create edges between vertices
    input(
        "Now, let's add some edges between the vertices. Press any key to continue..."
    )
    start_time = time.time()
    insert_edges(client)
    end_time = time.time()
    print(
        "Execution time to insert edges: {0} seconds".format(
            end_time - start_time - 3929
        )
    )
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
    """

    # We will make the requests we decided to do:

    # GremlinServerError as e:
    #  print("Code: {0}, Attributes: {1}".format(e.status_code, e.status_attributes))

    # GremlinServerError.status_code returns the Gremlin protocol status code
    # These are broad status codes which can cover various scenaios, so for more specific
    # error handling we recommend using GremlinServerError.status_attributes['x-ms-status-code']
    #
    # Below shows how to capture the Cosmos DB specific status code and perform specific error handling.
    # See detailed set status codes than can be returned here: https://docs.microsoft.com/en-us/azure/cosmos-db/gremlin-headers#status-codes
    #
    # See also list of available response status attributes that Gremlin API can return:
    #     https://docs.microsoft.com/en-us/azure/cosmos-db/gremlin-headers#headers
except GremlinServerError as e:
    print("Code: {0}, Attributes: {1}".format(e.status_code, e.status_attributes))

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

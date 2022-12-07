"""
for arangoDB :

# Create a new graph named "stack-overflow-english".
if not db.has_graph("stack-overflow-english"):
    graph = db.create_graph("stack-overflow-english")
else:
    graph = db.graph("stack-overflow-english")


# Create vertex collections for the graph.
if not graph.has_vertex_collection("posts"):
    posts = graph.create_vertex_collection("posts")

    for index, row in pd_posts_full.iterrows():
        posts.insert(
            {
                "_key": str(row["postId:ID(Post)"]),
                "title": row["title"],
                "score": row["score"],
                "views": row["views"],
                "comments": row["comments"],
            }
        )
else:
    posts = graph.vertex_collection("posts")

if not graph.has_vertex_collection("tags"):
    tags = graph.create_vertex_collection("tags")

    for index, row in pd_tags_full.iterrows():
        tags.insert(
            {
                "_key": row["tagId:ID(Tag)"],
                "tag": row["tagId:ID(Tag)"],
            }
        )
else:
    tags = graph.vertex_collection("tags")

if not graph.has_vertex_collection("users"):
    users = graph.create_vertex_collection("users")
    for index, row in pd_users_full.iterrows():
        users.insert(
            {
                "_key": str(row["userId:ID(User)"]),
                "name": row["displayname"],
                "reputation": row["reputation"],
                "views": row["views"],
                "upvotes": row["upvotes"],
                "downvotes": row["downvotes"],
            }
        )

else:
    users = graph.vertex_collection("users")

# Create an edge definition (relation) for the graph with the name "posts_rel".
if not graph.has_edge_definition("posts_rel"):
    posts_rel = graph.create_edge_definition(
        edge_collection="posts_rel",
        from_vertex_collections=["posts"],
        to_vertex_collections=["posts"],
    )

    for index, row in pd_posts_rel_full.iterrows():
        print(row[":START_ID(Post)"], row[":END_ID(Post)"])
        posts_rel.insert(
            {
                "_from": "posts/" + str(row[":START_ID(Post)"]),
                "_to": "posts/" + str(row[":END_ID(Post)"]),
                "type": "PARENT_OF",
            }
        )

# Create an edge definition (relation) for the graph with the name "tags_posts_rel".
if not graph.has_edge_definition("tags_posts_rel"):
    tags_posts_rel = graph.create_edge_definition(
        edge_collection="tags_posts_rel",
        from_vertex_collections=["tags"],
        to_vertex_collections=["posts"],
    )

    for index, row in pd_tags_posts_rel_full.iterrows():
        tags_posts_rel.insert(
            {
                "_from": "posts/" + str(row[":START_ID(Post)"]),
                "_to": "tags/" + str(row[":END_ID(Tag)"]),
                "type": "HAS_TAG",
            }
        )

# Create an edge definition (relation) for the graph with the name "users_posts_rel".
if not graph.has_edge_definition("users_posts_rel"):
    users_posts_rel = graph.create_edge_definition(
        edge_collection="users_posts_rel",
        from_vertex_collections=["users"],
        to_vertex_collections=["posts"],
    )

    for index, row in pd_users_posts_rel_full.iterrows():
        users_posts_rel.insert(
            {
                "_from": "users/" + str(row[":START_ID(User)"]),
                "_to": "posts/" + str(row[":END_ID(Post)"]),
                "type": "POSTED",
            }
        )
"""

# For CosmosDB with Gremlin API

from data.datasets import (pd_posts_full, pd_posts_rel_full, pd_tags_full,
                           pd_tags_posts_rel_full, pd_users_full,
                           pd_users_posts_rel_full)
from gremlin_python.driver import client, serializer, protocol
from gremlin_python.driver.protocol import \
    GremlinServerError  # GremlinServerError is raised when the server returns an error.
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.traversal import T, Order, P, Cardinality, Scope

from decouple import config

import asyncio
import sys
import time
import traceback

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # This is required on Windows to avoid the following error:
    # RuntimeError: There is no current event loop in thread 'Thread-1'.


COSMODB_ENDPOINT = config("COSMODB_ENDPOINT")
COSMODB_DATABASE = config("COSMODB_DATABASE")
COSMODB_GRAPH = config("COSMODB_GRAPH")
COSMODB_PASSWORD = config("COSMODB_PASSWORD")


# Graph graph_so has already been created in the Azure portal.

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

def cleanup_value(value):
    # This function cleans up the query string to remove any new lines and extra spaces.
    # This is required to avoid Gremlin syntax errors.
    if value is None:
        return 0
    if value == "nan":
        return 0
    elif value == " nan":
        return 0
    elif value == "nan ":
        return 0
    elif value == " nan ":
        return 0
    # starts with nan
    elif type(value) == str and value.startswith("nan"):
        return 0
    else:
        print(f"[{value}]")
    return value.replace(
                "nan", "0"
            ).replace(
                "'", r"\'"
            ) if type(value) == str else value

def create_insert_vertices_query():
    # Create a Gremlin query to insert vertices into the graph.
    
    queries = []

    for index, row in pd_posts_full.iterrows():
        queries.append(
            f"g.addV('post').property('pk', '{cleanup_value(row['postId:ID(Post)'])}').property('title', '{cleanup_value(row['title'])}').property('score', {cleanup_value(row['score'])}).property('views', {cleanup_value(row['views'])}).property('comments', {cleanup_value(row['comments'])})"
        )

    """
    for index, row in pd_tags_full.iterrows():
        tags.insert(
            {
                "_key": row["tagId:ID(Tag)"],
                "tag": row["tagId:ID(Tag)"],
            }
        )
    """

    for index, row in pd_tags_full.iterrows():
        queries.append(
            f"g.addV('tag').property('pk', '{cleanup_value(row['tagId:ID(Tag)'])}')"
        )

    """
        for index, row in pd_users_full.iterrows():
        users.insert(
            {
                "_key": str(row["userId:ID(User)"]),
                "name": row["displayname"],
                "reputation": row["reputation"],
                "views": row["views"],
                "upvotes": row["upvotes"],
                "downvotes": row["downvotes"],
            }
        )
    """

    for index, row in pd_users_full.iterrows():
        queries.append(
            f"g.addV('user').property('pk', '{cleanup_value(row['userId:ID(User)'])}').property('name', '{cleanup_value(row['displayname'])}').property('reputation', {cleanup_value(row['reputation'])}).property('views', {cleanup_value(row['views'])}).property('upvotes', {cleanup_value(row['upvotes'])}).property('downvotes', {cleanup_value(row['downvotes'])})"
        )



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


_gremlin_insert_vertices = create_insert_vertices_query()
print(len(_gremlin_insert_vertices))

# count execution time
start_time = time.time()


try:
    inp = input("We're about to insert the vertices. Press y to continue...")
    if inp == "y":
        
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

stop_time = time.time()

print("Execution time: {0} seconds".format(stop_time - start_time))

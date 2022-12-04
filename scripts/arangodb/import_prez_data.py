# -*- coding: utf-8 -*-
from connection import client
from decouple import config

from data.datasets import (pd_posts_full, pd_posts_rel_full, pd_tags_full,
                           pd_tags_posts_rel_full, pd_users_full,
                           pd_users_posts_rel_full)

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

## Queries
# 1. The Top 10 Stack Overflow Users - ok
"""
FOR u IN users
    SORT u.reputation DESC
    LIMIT 10
    RETURN u
"""

# 2. The Top 5 tags That Sven Yargs Used in Asking Questions - not ok
"""
FOR u IN users
    FILTER u.name == "Sven Yargs"
    FOR p IN 1..1 OUTBOUND u users_posts_rel
        FOR t IN 1..1 INBOUND p tags_posts_rel
            RETURN t.tag
"""

# 3. How Sven Yargs Connected to Robusto?
"""
FOR u IN users
    FILTER u.name == "Sven Yargs"
    FOR p IN 1..1 OUTBOUND u users_posts_rel
        FOR t IN 1..1 INBOUND p tags_posts_rel
            FOR u2 IN 1..1 INBOUND t tags_posts_rel
                FILTER u2.name == "Robusto"
                RETURN u2
"""

# 4. The top 10 People Who Posted the Most Questions about grammar
"""
FOR t IN tags
    FILTER t.tag == "grammar"
    FOR p IN 1..1 INBOUND t tags_posts_rel
        FOR u IN 1..1 INBOUND p users_posts_rel
            RETURN u
"""

# 5. Which Users Answered Their Own Questions?
"""
FOR u IN users
    FOR p IN 1..1 OUTBOUND u users_posts_rel
        FOR p2 IN 1..1 INBOUND p posts_rel
            FILTER p2._key == p._key
            RETURN u
"""

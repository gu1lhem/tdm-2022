# -*- coding: utf-8 -*-
"""
Module that will create many datasets from the original one. The idea is to obtain different sized datasets
"""

from pathlib import Path

from decouple import config

from data.data_treatment import clear_data, get_data

path = config("PATH_TO_DATA")
path = Path(path)
pd_posts_full = clear_data(get_data(path / "posts.csv"))
pd_posts_full = pd_posts_full.drop(columns=["body"])
# Get the ids where there is a null value
null_ids = pd_posts_full[pd_posts_full.isnull().any(axis=1)].index
pd_users_full = clear_data(get_data(path / "users.csv"))
pd_tags_full = clear_data(get_data(path / "tags.csv"))
pd_posts_rel_full = clear_data(get_data(path / "posts_rel.csv"))
# Remove the posts that have a null value
pd_posts_rel_full = pd_posts_rel_full[
    ~pd_posts_rel_full[":START_ID(Post)"].isin(null_ids)
]
pd_tags_posts_rel_full = clear_data(get_data(path / "tags_posts_rel.csv"))
# Remove the posts that have a null value
pd_tags_posts_rel_full = pd_tags_posts_rel_full[
    ~pd_tags_posts_rel_full[":START_ID(Post)"].isin(null_ids)
]
pd_users_posts_rel_full = clear_data(get_data(path / "users_posts_rel.csv"))
# Remove the posts that have a null value
pd_users_posts_rel_full = pd_users_posts_rel_full[
    ~pd_users_posts_rel_full[":END_ID(Post)"].isin(null_ids)
]

# Keep only the lines where the id is < 100
pd_posts_100 = pd_posts_full[pd_posts_full["postId:ID(Post)"] < 100]
pd_posts_rel_100 = pd_posts_rel_full[pd_posts_rel_full[":START_ID(Post)"] < 100]
pd_tags_posts_rel_100 = pd_tags_posts_rel_full[
    pd_tags_posts_rel_full[":START_ID(Post)"] < 100
]
pd_users_posts_rel_100 = pd_users_posts_rel_full[
    pd_users_posts_rel_full[":END_ID(Post)"] < 100
]

# Keep only the lines where the id is < 1000
pd_posts_1000 = pd_posts_full[pd_posts_full["postId:ID(Post)"] < 1000]
pd_posts_rel_1000 = pd_posts_rel_full[pd_posts_rel_full[":START_ID(Post)"] < 1000]
pd_tags_posts_rel_1000 = pd_tags_posts_rel_full[
    pd_tags_posts_rel_full[":START_ID(Post)"] < 1000
]
pd_users_posts_rel_1000 = pd_users_posts_rel_full[
    pd_users_posts_rel_full[":END_ID(Post)"] < 1000
]

# Keep only the lines where the id is < 5000
pd_posts_5000 = pd_posts_full[pd_posts_full["postId:ID(Post)"] < 5000]
pd_posts_rel_5000 = pd_posts_rel_full[pd_posts_rel_full[":START_ID(Post)"] < 5000]
pd_tags_posts_rel_5000 = pd_tags_posts_rel_full[
    pd_tags_posts_rel_full[":START_ID(Post)"] < 5000
]
pd_users_posts_rel_5000 = pd_users_posts_rel_full[
    pd_users_posts_rel_full[":END_ID(Post)"] < 5000
]

# Keep only the lines where the id is < 10000
pd_posts_10000 = pd_posts_full[pd_posts_full["postId:ID(Post)"] < 10000]
pd_posts_rel_10000 = pd_posts_rel_full[pd_posts_rel_full[":START_ID(Post)"] < 10000]
pd_tags_posts_rel_10000 = pd_tags_posts_rel_full[
    pd_tags_posts_rel_full[":START_ID(Post)"] < 10000
]
pd_users_posts_rel_10000 = pd_users_posts_rel_full[
    pd_users_posts_rel_full[":END_ID(Post)"] < 10000
]

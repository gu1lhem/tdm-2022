# -*- coding: utf-8 -*-
import json

import requests
from connection import client

db = client.db("GOT", username="root", password="Password")
aql = db.aql

if db.has_collection("Characters"):
    Characters = db.collection("Characters")
else:
    Characters = db.create_collection("Characters")

cursor = aql.execute(
    "INSERT {"
    '"name": "Ned",'
    '"surname": "Stark",'
    '"alive": true,'
    '"age": 41,'
    '"traits": ["A","H","C","N","P"]'
    "} INTO Characters"
)


print(db["Characters"])

print("----------------------------------------")
cursor = aql.execute(
    'LET data = [\
    { "name": "Robert", "surname": "Baratheon", "alive": false, "traits": ["A","H","C"] },\
    { "name": "Jaime", "surname": "Lannister", "alive": true, "age": 36, "traits": ["A","F","B"] },\
    { "name": "Catelyn", "surname": "Stark", "alive": false, "age": 40, "traits": ["D","H","C"] },\
    { "name": "Cersei", "surname": "Lannister", "alive": true, "age": 36, "traits": ["H","E","F"] },\
    { "name": "Daenerys", "surname": "Targaryen", "alive": true, "age": 16, "traits": ["D","H","C"] },\
    { "name": "Jorah", "surname": "Mormont", "alive": false, "traits": ["A","B","C","F"] },\
    { "name": "Petyr", "surname": "Baelish", "alive": false, "traits": ["E","G","F"] },\
    { "name": "Viserys", "surname": "Targaryen", "alive": false, "traits": ["O","L","N"] },\
    { "name": "Jon", "surname": "Snow", "alive": true, "age": 16, "traits": ["A","B","C","F"] },\
    { "name": "Sansa", "surname": "Stark", "alive": true, "age": 13, "traits": ["D","I","J"] },\
    { "name": "Arya", "surname": "Stark", "alive": true, "age": 11, "traits": ["C","K","L"] },\
    { "name": "Robb", "surname": "Stark", "alive": false, "traits": ["A","B","C","K"] },\
    { "name": "Theon", "surname": "Greyjoy", "alive": true, "age": 16, "traits": ["E","R","K"] },\
    { "name": "Bran", "surname": "Stark", "alive": true, "age": 10, "traits": ["L","J"] },\
    { "name": "Joffrey", "surname": "Baratheon", "alive": false, "age": 19, "traits": ["I","L","O"] },\
    { "name": "Sandor", "surname": "Clegane", "alive": true, "traits": ["A","P","K","F"] },\
    { "name": "Tyrion", "surname": "Lannister", "alive": true, "age": 32, "traits": ["F","K","M","N"] },\
    { "name": "Khal", "surname": "Drogo", "alive": false, "traits": ["A","C","O","P"] },\
    { "name": "Tywin", "surname": "Lannister", "alive": false, "traits": ["O","M","H","F"] },\
    { "name": "Davos", "surname": "Seaworth", "alive": true, "age": 49, "traits": ["C","K","P","F"] },\
    { "name": "Samwell", "surname": "Tarly", "alive": true, "age": 17, "traits": ["C","L","I"] },\
    { "name": "Stannis", "surname": "Baratheon", "alive": false, "traits": ["H","O","P","M"] },\
    { "name": "Melisandre", "alive": true, "traits": ["G","E","H"] },\
    { "name": "Margaery", "surname": "Tyrell", "alive": false, "traits": ["M","D","B"] },\
    { "name": "Jeor", "surname": "Mormont", "alive": false, "traits": ["C","H","M","P"] },\
    { "name": "Bronn", "alive": true, "traits": ["K","E","C"] },\
    { "name": "Varys", "alive": true, "traits": ["M","F","N","E"] },\
    { "name": "Shae", "alive": false, "traits": ["M","D","G"] },\
    { "name": "Talisa", "surname": "Maegyr", "alive": false, "traits": ["D","C","B"] },\
    { "name": "Gendry", "alive": false, "traits": ["K","C","A"] },\
    { "name": "Ygritte", "alive": false, "traits": ["A","P","K"] },\
    { "name": "Tormund", "surname": "Giantsbane", "alive": true, "traits": ["C","P","A","I"] },\
    { "name": "Gilly", "alive": true, "traits": ["L","J"] },\
    { "name": "Brienne", "surname": "Tarth", "alive": true, "age": 32, "traits": ["P","C","A","K"] },\
    { "name": "Ramsay", "surname": "Bolton", "alive": true, "traits": ["E","O","G","A"] },\
    { "name": "Ellaria", "surname": "Sand", "alive": true, "traits": ["P","O","A","E"] },\
    { "name": "Daario", "surname": "Naharis", "alive": true, "traits": ["K","P","A"] },\
    { "name": "Missandei", "alive": true, "traits": ["D","L","C","M"] },\
    { "name": "Tommen", "surname": "Baratheon", "alive": true, "traits": ["I","L","B"] },\
    { "name": "Jaqen", "surname": "Hghar", "alive": true, "traits": ["H","F","K"] },\
    { "name": "Roose", "surname": "Bolton", "alive": true, "traits": ["H","E","F","A"] },\
    { "name": "The High Sparrow", "alive": true, "traits": ["H","M","F","O"] }\
    ]\
    FOR d IN data INSERT d INTO Characters'
)

# Print all characters from Python Driver
for character in db.collection("Characters"):
    print("- %s" % character["name"])

print("----------------------------------------")
cursor = aql.execute(
    "INSERT {"
    '"name": "Robert",'
    '"surname": "Baratheon",'
    '"alive": false,'
    '"traits": ["A","H","C"]'
    "} INTO Characters"
)
cursor = aql.execute(
    "INSERT {"
    '"name": "Jaime",'
    '"surname": "Lannister",'
    '"alive": true,'
    '"age": 36,'
    '"traits": ["A","F","B"]'
    "} INTO Characters"
)

print(cursor)
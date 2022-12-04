# TDR Project

Rédaction d'un rapport (20 pages max) expliquant :

- La motivation de vos choix des moteurs à comparer.
- Les étapes à suivre pour pouvoir installer et/ou utiliser chaque moteur.
- La structure de votre jeu de donnée et la description des cas d’usages.
- Les étapes de création ou de chargement de votre jeu de données dans chaque
  moteur.
- L’expression de vos requêtes pour chaque moteur, le résultat obtenu et leurs temps
  d’exécution pour des jeux de données de différentes tailles.
- Une comparaison des moteurs en termes d’installation/utilisation par rapport à
  votre jeu de données et de vos cas d’usage.
- L’analyse théorique de chaque moteur (à réaliser de manière individuelle – un moteur
  par personne) et un comparatif de ces analyses.
- Une conclusion indiquant les difficultés rencontrées, la répartition du travail entre les
  membres du groupe et le temps passé sur ce projet.

## TODO Cas d'usage

- [x] Installation des systèmes de BD
- [x] Nettoyer les données
  - Deux entités, une ville avec tous le nombre d'inscrits, d'abstention, etc... et les candidats
- [ ] Importer les données dans tous les systèmes de BD:
  - [ ] arangoDB
  - [ ] CosmoDB
  - [ ] janusGraph
- [ ] Point de vue Utilisateur standard : Vous devez pour cela définir, en langage courant, 4 types
      d’interrogations sur votre jeu de données. On estimera que celles-ci sont effectuées très
      fréquemment 1. Les dix communes où il y a le plus d'inscrits 2. Le score d'Emmanuel Macron à Paris 3. Pour chaque candidat, la communes où il a fait le meilleur résultat 4. Les résultats des communes dans laquelle l'abstention est supérieure à 50%
- [ ] Point de vue Analyste de données : Vous devez pour cela définir, en langage courant, 2 types
      d’interrogations complexes sur votre jeu de données (agrégation, transformation, calcul
      complexe) 1. Obtenir les gagnants dans chaque département -> agrégation et calcul 2. Transformer le pourcentage exprimés pour chaque candidat par rappoort aux nombres d'inscrits et non plus d'exprimés
- [ ] Tester le temps d'exécution des requêtes
- [ ] **Ne pas oublier l'analyse théorique à réaliser individuellement**

## Dataset StackOverflow
--nodes:Post csvs/posts.csv \
--nodes:User csvs/users.csv \
--nodes:Tag csvs/tags.csv \
--relationships:PARENT_OF csvs/posts_rel.csv \
--relationships:ANSWER csvs/posts_answers.csv \
--relationships:HAS_TAG csvs/tags_posts_rel.csv \
--relationships:POSTED csvs/users_posts_rel.csv

## Installation

### Env installation

#### With requirements.txt

```bash
python -m venv env
.\env\Scripts\activate
pip install -r requirements.txt
pre-commit install
```

#### With setup.py

```bash
python -m venv env
.\env\Scripts\activate
pip install -e .
```

If you want to install specific dependencies, you can use the following command:

```bash
pip install -e .[arangodb]/[janusgraph]/[cosmodb]
```

### Docker

#### For arangoDB:

```bash
docker-compose up arangodb
```

Then go to localhost:8529 to access the arangoDB web interface.
You can use the username and password (root:Password) to login.

#### For janusgraph:

```bash
docker-compose up janusgraph
```

Then access to the gremlin console with:

```bash
docker-compose exec janusgraph bin/gremlin.sh ./janus-graph-server-configuration.yaml
```
To connect the console to the database in the Gremlin console
```bash
:remote connect tinkerpop.server conf/remote.yaml
:remote console
```

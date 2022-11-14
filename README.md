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
- [X] Installation des systèmes de BD
- [ ] Importer les données dans tous les systèmes de BD:
    - [ ] arangoDB
    - [ ] CosmoDB
    - [ ] janusGraph
- [ ] Point de vue Utilisateur standard : Vous devez pour cela définir, en langage courant, 4 types
d’interrogations sur votre jeu de données. On estimera que celles-ci sont effectuées très
fréquemment
- [ ] Point de vue Analyste de données : Vous devez pour cela définir, en langage courant, 2 types
d’interrogations complexes sur votre jeu de données (agrégation, transformation, calcul
complexe)
- [ ] Tester le temps d'exécution des requêtes
- [ ] **Ne pas oublier l'analyse théorique à réaliser individuellement**

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
docker-compose exec janusgraph bin/gremlin.sh
```

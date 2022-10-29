# TDR Project

## Installation

### Env installation
```bash
python -m venv env
.\env\Scripts\activate
pip install -r requirements.txt
pre-commit install
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

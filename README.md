# DataScientest.Project3
- Get data
- Choose appropriate DB
- Load data into DB
- Create API to play with data
- :-)

# Data
https://www.kaggle.com/datasets/konivat/tree-of-life

# Run API
uvicorn Main:api --reload

# Run Neo4J (official and latest)
```
docker run -d -it --rm \  
    --name Neo4jForProject3 \  
    -p 7474:7474 \  
    -p 7687:7687 \  
    -v $PWD/data:/import \  
    -v $PWD/neo4j/database:/data \  
    -v $PWD/neo4j/plugins:/plugins \  
    -v $PWD/neo4j/conf:/conf \  
    -e NEO4J_AUTH=neo4j/s3cr3t \  
    -e NEO4JLABS_PLUGINS='["apoc","graph-data-science"]' \  
    neo4j:latest
```
''' docker run -d -it --rm --name Neo4jForProject3 -p 7474:7474 -p 7687:7687 -v $PWD/data:/import -v $PWD/neo4j/database:/data -v $PWD/neo4j/plugins:/plugins -v $PWD/neo4j/conf:/conf -e NEO4J_AUTH=neo4j/s3cr3t -e NEO4JLABS_PLUGINS='["apoc","graph-data-science"]' neo4j:latest '''

### Plugins:
- Set into 'plugins' folder redirection
- Config to allow plugins' procedures in 'conf' folder redirection
- From:
  - https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/4.4.0.6
  - https://neo4j.com/graph-data-science-software/

### Import folder redirection:
- In order to load local file instead of having a public git with distant acces to CSV files

### Data folder redirection:
- In order to save loaded database and not having to reload it all the time



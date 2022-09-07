FROM python:3.10.4-slim

COPY ./api /home/lifeproject/api
COPY ./data /home/lifeproject/data
COPY ./datascience /home/lifeproject/datascience
COPY ./loader /home/lifeproject/loader
COPY ./neo4j /home/lifeproject/neo4j
COPY Main.py  /home/lifeproject/
COPY README.md /home/lifeproject/
COPY requirements.txt /home/lifeproject/

RUN apt update && apt install curl -y
RUN pip install -r /home/lifeproject/requirements.txt

WORKDIR /home/lifeproject/

EXPOSE 8000

CMD docker run -d -it --rm --name Neo4jForProject3 -p 7474:7474 -p 7687:7687 -v $PWD/data:/import -v $PWD/neo4j/database:/data -v $PWD/neo4j/plugins:/plugins -v $PWD/neo4j/conf:/conf -e NEO4J_AUTH=neo4j/s3cr3t -e NEO4JLABS_PLUGINS='["apoc","graph-data-science"]' neo4j:latest
CMD uvicorn main:api --host 0.0.0.0
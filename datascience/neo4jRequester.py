from neo4j import GraphDatabase

##################################################################################
### Query template
##################################################################################

shortestPathQuery = """
MATCH (start:LifeNode {{ name: '{species1}' }})
MATCH (end:LifeNode {{ name: '{species2}' }})
MATCH path = shortestPath((start)-[*..]->(end))
RETURN start, end, path
"""

alternativeShortestPathQuery = """
MATCH (start:LifeNode {name: 'Gorilla gorilla'})
MATCH (end:LifeNode {name: 'Sand lizards'})
CALL gds.shortestPath.dijkstra.stream("tree_of_life", {
 sourceNode: id(start),
 targetNode: id(end)
})
YIELD index,sourceNode,targetNode,totalCost,nodeIds,costs,path
RETURN path
"""

modifInfoNodeQuery = """
MATCH (s: LifeNode {{ name: '{specie}' }})
SET s.{'{parameter}'} = {'{value}'}
RETURN s
"""

ajoutNode = """
MERGE (s: LifeNode {{ name: '{name}',
                      number_of_child: '{number_of_child}',
                      is_leaf_node: '{is_leaf_node}'
                      is_extinct: '{is_extinct}'
                      confidence: '{confidence}'
                      phylesis: '{phylesis}'
                      tolorg_link: '{tolorg_link}'
                      }})
RETURN s
"""

ajoutRelationship = """
MATCH (start: LifeNode {{ name: '{species1}'}})
MATCH (end: LifeNode {{ name: '{species2}'}})
MERGE (start)-[r: {'{relationship}'}]->(end)
RETURN start, end, r

"""



##################################################################################
### Neo4J request methods
##################################################################################

driver = GraphDatabase.driver("bolt://127.0.0.1:7687", auth=("neo4j", "s3cr3t"))


def getShortestPathBetween(species1: str, species2: str):
    shortestPath = []
    with driver.session() as session:
        result = session.run(shortestPathQuery.format(species1=species1, species2=species2))
        for res in result:
            shortestPath.append(res["start"]["name"])
            for rel in res["path"].relationships:
                shortestPath.append(
                    [rel.nodes[0]["name"], rel.type, rel.nodes[1]["name"]]
                )
            shortestPath.append(res["end"]["name"])
    return shortestPath


def getModifInfoNode(specie: str, parameter: str, value):
    modifNode = []
    with driver.session() as session:
        result = session.run(
            modifInfoNodeQuery.format(specie=specie, parameter=parameter, value=value)
        )
        for res in result:
            modifNode.append(res["s"]["name"])
            modifNode.append(res["s"]["{parameter}"])
        return modifNode

def getAjoutNode(name: str, number_of_child: int, is_leaf_node: int, is_extinct: int, confidence: int, phylesis: int, tolorg_link: int):
    ajoutNode = []
    with driver.session()as session:
        result = session.run(
            ajoutInfoNodeQuery.format(name = name, number_of_child = number_of_child, is_leaf_node = is_leaf_node, is_extinct = is_extinct, confidence = confidence, phylesis = phylesis, tolorg_link = tolorg_link)
            )
        for res in result:
            ajoutNode.append(res["s"]["name"])
            ajoutNode.append(res["s"]["number_of_child"])
            ajoutNode.append(res["s"]["is_leaf_node"])
            ajoutNode.append(res["s"]["is_extinct"])
            ajoutNode.append(res["s"]["confidence"])
            ajoutNode.append(res["s"]["phylesis"])
            ajoutNode.append(res["s"]["tolorg_link"])
        return ajoutNode

def getAjoutRelationship(species1: str, species2: str, relationship: str):
    ajoutRelationship = []
    with driver.session()as session:
        result = session.run(
            ajoutRelationship.format(species1 = species1, species2 = species2, relationship = relationship)
        )
        for res in result:
            ajoutRelationship.append(res["start"]["name"])
            ajoutRelationship.append(res["end"]["name"])
            ajoutRelationship.append(res["r"]["type"])
        return ajoutRelationship
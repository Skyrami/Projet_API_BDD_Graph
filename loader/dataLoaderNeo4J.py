from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://127.0.0.1:7687", auth=("neo4j", "s3cr3t"))

# #########################################################
# Delete previously created data
# #########################################################
print("Deleting previous data")
with driver.session() as session:
    session.run("MATCH (n) DETACH DELETE n;")
    session.run("CALL gds.graph.drop('tree_of_life', false);")


# #########################################################
# Set a unicity constraint on provided Node ID (= 'nid')
# #########################################################
print("Defining constraint on 'nid'")
with driver.session() as session:
    session.run(
        "CREATE CONSTRAINT nidConstraint IF NOT EXISTS FOR (n:LifeNode) REQUIRE n.nid IS UNIQUE;"
    )


# #########################################################
# Insert nodes
# #########################################################
print("Inserting life node")
insertLifeNodeQuery = """
USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS 
FROM 'file:///treeoflife_nodes.csv'
AS row
CREATE (:LifeNode {
        nid: toInteger(row.node_id),
        name: row.node_name,
        number_of_child: toInteger(row.child_nodes),
        is_leaf_node: row.leaf_node,
        is_extinct: row.extinct,
        confidence: row.confidence,
        phylesis: row.phylesis,
        tolorg_link: row.tolorg_link
    });
"""
with driver.session() as session:
    session.run(insertLifeNodeQuery)


# #########################################################
# Importing relation between nodes
# #########################################################
print("Creating relation between life node")
insertLifeNodeRelationQuery = """
USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS 
FROM 'file:///treeoflife_links.csv' 
AS row
MATCH (ancestor:LifeNode {nid: toInteger(row.source_node_id)}) 
MATCH (descendant:LifeNode {nid: toInteger(row.target_node_id)})
CREATE (ancestor)-[:PARENT_OF]->(descendant)
CREATE (descendant)-[:CHILD_OF]->(ancestor);
"""
with driver.session() as session:
    session.run(insertLifeNodeRelationQuery)


# #########################################################
# Rename node with no provided name by their Node ID
# #########################################################
print("Rename 'unnamed' life node with their Node ID")
with driver.session() as session:
    session.run("MATCH (n {name:'none'}) set n.name = 'Unknown_'+n.nid return n;")


# #########################################################
# Transform 'is_extinct' property into 'Alive'/'Extinct' labels
# #########################################################
print("Transform some properties as labels")
movePropertyToLabelQuery = """
MATCH (n {{ is_leaf_node:'0', is_extinct: '{propertyValue}' }})
CALL apoc.create.addLabels([id(n)], ['{newLabelName}']) 
YIELD node
RETURN node;
"""
with driver.session() as session:
    session.run(
        movePropertyToLabelQuery.format(propertyValue="0", newLabelName="Alive")
    )
    session.run(
        movePropertyToLabelQuery.format(propertyValue="1", newLabelName="Extinct")
    )


# #########################################################
# Declare a graph on all nodes for future request with GDS plugin
# #########################################################
print("Create and name a graph with imported data")
with driver.session() as session:
    session.run("CALL gds.graph.project('tree_of_life','*','*');")
# To check that graph is properly created: "CALL gds.graph.list() YIELD graphName"

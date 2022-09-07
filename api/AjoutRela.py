from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel

import datascience.neo4jRequester as neo4jRequester


class requestBody(BaseModel):
    species1: str = "Homo sapiens"
    species2: str = "Pongo abelii"
    relationship: str = "PARENT_OF"

def doGetAjoutRelationship(species1: str, species2: str, relationship: str): 
    # TODO: Get closest species ID from approximative species names given by users...
    return neo4jRequester.getAjoutRelationship(species1, species2, relationship)


####################################################################################################
#####   API definition
####################################################################################################

rootVerb = "/datascientest/lifeproject"
verb = "/ajoutrelationship"
name = "Ajout Relationship"
tags = ["ajoutrelationship"]
responses = {
    200: {"description": "Add a relationship between 2 nodes"},
    404: {"description": "Not found"},
}


router = APIRouter(
    prefix=rootVerb,
    tags=tags,
)


@router.get(verb, name=name, responses=responses)
async def getAjoutRelationship(species1: Optional[str] = "Homo sapiens", species2: Optional[str] = "Pongo abelii", relationship: Optional[str] = "PARENT_OF"):
    return doGetAjoutRelationship(species1, species2, relationship)


@router.post(verb, name=name, responses=responses)
async def postShortestPath(requestBody: requestBody):
    return doGetAjoutRelationship(requestBody.species1, requestBody.species2, requestBody.relationship)
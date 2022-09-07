from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel

import datascience.neo4jRequester as neo4jRequester


class requestBody(BaseModel):
    species1: str = "Homo sapiens"
    species2: str = "Pongo abelii"

def doGetShortestPath(species1: str, species2: str): 
    # TODO: Get closest species ID from approximative species names given by users...
    return neo4jRequester.getShortestPathBetween(species1, species2)


####################################################################################################
#####   API definition
####################################################################################################

rootVerb = "/datascientest/lifeproject"
verb = "/shortestpath"
name = "Shortest Path"
tags = ["shortestpath"]
responses = {
    200: {"description": "Get shortest path into life tree between two species"},
    404: {"description": "Not found"},
}


router = APIRouter(
    prefix=rootVerb,
    tags=tags,
)


@router.get(verb, name=name, responses=responses)
async def getShortestPath(species1: Optional[str] = "Homo sapiens", species2: Optional[str] = "Pongo abelii"):
    return doGetShortestPath(species1, species2)


@router.post(verb, name=name, responses=responses)
async def postShortestPath(requestBody: requestBody):
    return doGetShortestPath(requestBody.species1, requestBody.species2)

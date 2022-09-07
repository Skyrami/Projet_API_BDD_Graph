from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel

import datascience.neo4jRequester as neo4jRequester


class requestBody(BaseModel):
    species1: str = "Homo sapiens"
    species2: str = "Pongo abelii"

def doGetCommonAncestor(species1: str, species2: str): 
    # TODO: Get closest species ID from approximative species names given by users...
    shortestPath = neo4jRequester.getShortestPathBetween(species1, species2)
    for subPath in shortestPath[1:-1]:
        if subPath[1] == 'PARENT_OF':
            return subPath[0]
    raise HTTPException(status_code=404, detail="Common ancestor not found...")


####################################################################################################
#####   API definition
####################################################################################################

rootVerb = "/datascientest/lifeproject"
verb = "/common-ancestor"
name = "Common Ancestor"
tags = ["ancestor"]
responses = {
    200: {"description": "Get common ancestor into life tree between two species"},
    404: {"description": "Not found"},
}


router = APIRouter(
    prefix=rootVerb,
    tags=tags,
)


@router.get(verb, name=name, responses=responses)
async def getCommonAncestor(species1: Optional[str] = "Homo sapiens", species2: Optional[str] = "Pongo abelii"):
    return doGetCommonAncestor(species1, species2)

@router.post(verb, name=name, responses=responses)
async def postCommonAncestor(requestBody: requestBody):
    return doGetCommonAncestor(requestBody.species1, requestBody.species2)

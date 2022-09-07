from http.client import responses
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional


import datascience.neo4jRequester as neo4jRequester

class requestBody(BaseModel):
    name : str = "Homo sapiens"
    number_of_child : int = 0
    is_leaf_node : int = 0
    is_extinct : int = 0
    confidence : int = 1
    phylesis : int = 1
    tolorg_link : int = 1

def doGetAjoutNode(name: str, number_of_child: int, is_leaf_node: int, is_extinct: int, confidence: int, phylesis: int, tolorg_link: int):
    return neo4jRequester.getAjoutNode(name, number_of_child, is_leaf_node, is_extinct, confidence, phylesis, tolorg_link)

####################################################################################################
#####   API definition
####################################################################################################

rootVerb = "/datascientest/lifeproject"
verb = "/modifinfonode"
name = "Modif Info Node"
tags = ["modifinfonode"]
responses = {
    200: {"description": "Modify the information of a node"},
    404: {"description": "Not found"},
}

router = APIRouter(
    prefix=rootVerb,
    tags=tags,
)

@router.get(verb, name=name, responses=responses)
async def getAjoutNode(name: Optional[str] = "Homo Sapiens", number_of_child: Optional[int] = 0, is_leaf_node: Optional[int] = 0 , is_extinct: Optional[int] = 0, confidence: Optional[int] = 0, phylesis: Optional[int] = 0, tolorg_link: Optional[int] = 0):
    return doGetAjoutNode(name, number_of_child, is_leaf_node, is_extinct, confidence, phylesis, tolorg_link)


@router.post(verb, name=name, responses=responses)
async def AjoutNode(requestBody: requestBody):
    return doGetAjoutNode(requestBody.name, requestBody.number_of_child, requestBody.is_leaf_node, requestBody.is_extinct, requestBody.confidence, requestBody.phylesis, requestBody.tolorg_link)
from http.client import responses
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional


import datascience.neo4jRequester as neo4jRequester

class requestBody(BaseModel):
    specie : str = "Homo sapiens"
    parameter : str = "number_of_child"
    value = 3

def doGetModifInfoNode(specie: str, parameter: str, value):
    return neo4jRequester.getModifInfoNode(specie, parameter, value)

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
async def getModifInfoNode(specie: Optional[str] = "Homo Sapiens", parameter: Optional[str] = "number_of_child", value: Optional[int] = 3):
    return doGetModifInfoNode(specie, parameter, value)


@router.post(verb, name=name, responses=responses)
async def modifyInfoNode(requestBody: requestBody):
    return doGetModifInfoNode(requestBody.specie, requestBody.parameter, requestBody.value)
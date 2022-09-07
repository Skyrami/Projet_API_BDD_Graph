from fastapi import FastAPI

from api import AjoutNode, StatusAPI, ShortestPathAPI, CommonAncestorAPI, ModifInfoNode, AjoutNode, AjoutRela

api = FastAPI()

api.include_router(StatusAPI.router)
api.include_router(ShortestPathAPI.router)
api.include_router(CommonAncestorAPI.router)
api.include_router(ModifInfoNode.router)
api.include_router(AjoutNode.router)
api.include_router(AjoutRela.router)

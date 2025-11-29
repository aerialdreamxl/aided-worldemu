import json
from string import Template

def processSysPrompt(characters:list,id:str)->str:
    characterInfo={}
    for c in characters:
        if c["id"]==id:
            characterInfo=c
    if characterInfo=={}:
        raise RuntimeError(id+" Not found")
    
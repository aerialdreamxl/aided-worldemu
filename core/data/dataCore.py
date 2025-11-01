import json
import os
from pathlib import Path

dataVersion=0
defaultAgentBackend={
    'type': "openai",
    'baseURL': "http://127.0.0.1:11434/v1",
    'model': "qwen3:30b",
    'apiKey': "ollama"
}

#数据新建逻辑
def newAgentCharacter()->dict:#新建数字人角色
    return {
        'version': dataVersion,
        'type': "agentCharacter",       #数字人
        'id': "template",               #字符串id
        'name': "",                     #名字
        'personality': "",              #人格描述
        'modeling': "",                 #外貌描述
        'emotion': "",                  #情感
        'lastTick': 0,                  #上次调用时的Tick
        'memory': [],                   #记忆
        'relations': [],                #关系
        'rawChatHistory': [],           #对话历史
        'externalFiles': [
            { 'key':'personality', 'format':"txt" },
            { 'key':'modeling', 'format':"txt" },
            { 'key':'rawChatHistory', 'format':"json" }
        ]
    }

def newInstance(instanceLevel:str="singleCharacter")->dict:#新建模拟识别单元"实例"
    data={
        'version': dataVersion,
        'type': "instance",
        'level': "",
        'backend': defaultAgentBackend,
        'name': "demo实例",
        'contains': [],
        'containsData': [],
        'externalFiles': [
            { 'key':'contains', 'format':"json" },
            { 'key':'containsData', 'format':"json" }
        ]
    }
    if instanceLevel in [ "singleCharacter" ]:
        data['level']=instanceLevel
        data['contains']=[ newAgentCharacter() ]
    else:
        raise RuntimeError(instanceLevel+" Not supported in this version")
    return data

#数据保存逻辑
def processExternalFilesSave(instancePath:Path, instance:dict):
    instancePath.mkdir(parents=True, exist_ok=True)
    for key in instance['externalFiles']:
        rawData=""
        dataFile=instancePath
        if key['format']=="json":
            rawData=json.dumps(instance[key['key']], ensure_ascii=False, indent=2)
            dataFile=Path(instancePath/(key['key']+".json"))
            instance[key['key']]=[]
        elif key['format']=="txt":
            rawData=instance[key['key']]
            dataFile=Path(instancePath/(key['key']+".txt"))
            instance[key['key']]=""
        else:
            raise RuntimeError("Errors in externalFiles")
        dataFile.write_text(rawData, encoding='utf-8')

def saveInstance( userDataPath:Path=Path("userdata"), instance:dict=newInstance() ):
    userDataPath=Path(userDataPath)
    instanceSavePath=Path(userDataPath/instance['name'])
    instanceSavePath.mkdir(parents=True, exist_ok=True)
    # 处理ExternalFiles的逻辑放在这之间
    for containedThing in instance['contains']:
        if containedThing['type'].endswith('Character'):
            characterPath=Path(instanceSavePath/"characters"/containedThing['id'])
            processExternalFilesSave(characterPath,containedThing)
        else:
            raise RuntimeError("Something went wrong in WEMU")
    processExternalFilesSave(instanceSavePath/"instance",instance)
    # 处理ExternalFiles的逻辑放在这之间
    instanceRaw=json.dumps(instance, ensure_ascii=False, indent=2)
    instanceJson=instanceSavePath/"wemuInstance.json"
    instanceJson.write_text(instanceRaw, encoding='utf-8')

#数据加载逻辑

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
def newAgentCharacter(id:str="demo",name:str="demo人物",personality:str="请编辑此设定字段后再加载该数字人",modeling:str="")->dict:#新建数字人角色
    return {
        'version': dataVersion,
        'type': "agentCharacter",       #数字人
        'id': id,               #字符串id
        'name': name,                     #名字
        'personality': personality,              #人格描述
        'modeling': modeling,                 #外貌描述
        'emotion': "平静",                  #情感
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

def newInstance(name:str="demo")->dict:#新建模拟识别单元"实例"
    data={
        'version': dataVersion,
        'type': "instance",
        'backend': defaultAgentBackend,
        'name': name,
        'characters': [],
        'rooms': [],
        'worlds': [],
        'history': [],
        'resume': [],
        'externalFiles': [
            { 'key':'characters', 'format':"json" },
            { 'key':'rooms', 'format':"json" },
            { 'key':'worlds', 'format':"json" },
            { 'key':'history', 'format':"json" }
        ]
    }
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

def saveInstance(userDataPath:Path=Path("userdata"), instance:dict=newInstance()):
    userDataPath=Path(userDataPath)
    instanceSavePath=Path(userDataPath/instance['name'])
    instanceSavePath.mkdir(parents=True, exist_ok=True)
    for key in ['rooms','worlds']:
        for containedThing in instance[key]:
            keyPath=Path(instanceSavePath/key)
            processExternalFilesSave(keyPath,containedThing)
    for containedThing in instance['characters']:
        characterPath=Path(instanceSavePath/"characters"/containedThing['id'])
        processExternalFilesSave(characterPath,containedThing)
    processExternalFilesSave(instanceSavePath/"instance",instance)
    instanceRaw=json.dumps(instance, ensure_ascii=False, indent=2)
    instanceJson=instanceSavePath/"wemuInstance.json"
    instanceJson.write_text(instanceRaw, encoding='utf-8')

#数据加载逻辑
def processExternalFilesLoad(instancePath:Path, instance:dict)->dict:
    extFileDir=Path(instancePath)
    if instance['type'].endswith("Character"):
        extFileDir=Path(extFileDir/instance['id'])
    for key in instance['externalFiles']:
        extFile=extFileDir
        if key['format']=="json":
            extFile=Path(extFileDir/(key['key']+".json"))
            with open(extFile, 'r', encoding='utf-8') as f:
                instance[key['key']]=json.load(f)
        elif key['format']=="txt":
            extFile=Path(extFileDir/(key['key']+".txt"))
            with open(extFile, 'r', encoding='utf-8') as f:
                instance[key['key']]=f.read()
    return instance

def loadInstance(instanceDir:Path)->dict:
    instanceDir=Path(instanceDir)
    instanceJsonPath=instanceDir/"wemuInstance.json"
    with open(instanceJsonPath, 'r', encoding='utf-8') as f:
        instance=json.load(f)
    instance=processExternalFilesLoad(instanceDir/"instance",instance)
    for key in ['rooms','worlds','characters']:
        for containedThing in instance[key]:
            instance[key]=processExternalFilesLoad(instanceDir/key,containedThing)
    return instance

#测试函数
def main():
    print("AgentData:",newAgentCharacter())
    print("InstanceData:",newInstance())
    print("Save testing...")
    test=newInstance()
    test['characters'].append(newAgentCharacter())
    test['worlds'].append({'name':'demoWorld','type':'world','externalFiles':[]})
    test['rooms'].append({'name':'demoRoom','type':'room','externalFiles':[]})
    saveInstance(instance=test)
    input("Press Enter to continue...")
    print("Load testing...")
    test=loadInstance(Path("userdata/demo"))
    print("Loaded data:",test)
    input("Press Enter to continue...")
    print("Testing Complete")

if __name__ == "__main__":
    print("DataCore Module Testing...")
    main()
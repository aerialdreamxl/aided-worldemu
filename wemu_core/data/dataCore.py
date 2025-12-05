import json
import os
from pathlib import Path

dataVersion=1
defaultAgentBackend={
    'lm-studio': { 'type': "openai", 'baseURL': "http://127.0.0.1:1234/v1", 'apiKey': "lm-studio" },
    'ollama': { 'type': "openai", 'baseURL': "http://127.0.0.1:11434/v1", 'apiKey': "ollama" }
}


#数据新建逻辑
def newAgentCharacter(id:str="demo",name:str="DEFAULT",personality:str="无",modeling:str="无")->dict:#新建数字人角色
    return {
        'version': dataVersion,
        'type': "agentCharacter",       #数字人
        'id': id,               #字符串id
        'name': name,                     #名字
        'personality': personality,              #人格描述
        'modeling': modeling,                 #外貌描述
        'warmupNotes': "",
        'emotion': "",                  #情感
        'lastTick': 0,                  #上次调用时的Tick
        'memory': [],                   #记忆
        'relations': [],                #关系
        'rawChatHistory': [],           #对话历史
        'externalFiles': [
            { 'key':'personality', 'savedir':["character","#*NAME*#"], 'format':"txt" },
            { 'key':'modeling', 'savedir':["character","#*NAME*#"], 'format':"txt" },
            { 'key':'rawChatHistory', 'savedir':["character","#*NAME*#"], 'format':"json" }
        ]
    }

def newInstance(name:str="demo")->dict:#新建模拟识别单元"实例"
    data={
        'version': dataVersion,
        'type': "instance",
        'backend': defaultAgentBackend['lm-studio'],
        'name': name,
        'characters': [],
        'rooms': [],
        'worlds': [],
        'history': [],
        'resume': [],
        'externalFiles': [
            { 'key':'characters', 'savedir':["character"], 'format':"json" },
            { 'key':'rooms', 'savedir':["room"], 'format':"json" },
            { 'key':'worlds', 'savedir':["world"], 'format':"json" },
            { 'key':'history', 'savedir':[], 'format':"json" }
        ]
    }
    return data

#数据保存逻辑
def processExternalFilesSave(instancePath:Path, instance:dict)->dict:
    fullPath=Path(instancePath).resolve()
    for ext in instance['externalFiles']:
        extPath=fullPath
        for extp in ext['savedir']:
            if extp=="#*NAME*#":
                extp=instance['id']
            extPath=extPath/extp
        extPath.mkdir(parents=True, exist_ok=True)
        extPath=Path(extPath/(ext['key']+"."+ext['format']))
        if ext['format']=='json':
            extData=instance[ext['key']]
            extRaw=json.dumps(extData, ensure_ascii=False, indent=2)
            extPath.write_text(extRaw, encoding="utf-8")
            instance[ext['key']]=[]
        else:
            extData=instance[ext['key']]
            extPath.write_text(extData, encoding="utf-8")
            instance[ext['key']]=""
    return instance

def saveInstance(userDataPath:Path=Path("userdata"), instance:dict=newInstance()):
    instancePath=Path(userDataPath/instance['name']).resolve()
    for a in ["characters","rooms","worlds"]:
        for b in instance[a]:
            b=processExternalFilesSave(instancePath,b)
    instance=processExternalFilesSave(instancePath,instance)
    instanceRaw=json.dumps(instance, ensure_ascii=False, indent=2)
    instanceJson=instancePath/"wemuInstance.json"
    instanceJson.write_text(instanceRaw, encoding='utf-8')

#数据加载逻辑
def processExternalFilesLoad(instancePath:Path, instance:dict)->dict:
    fullPath=Path(instancePath).resolve()
    for ext in instance['externalFiles']:
        extPath=fullPath
        for extp in ext['savedir']:
            if extp=="#*NAME*#":
                extp=instance['id']
            extPath=extPath/extp
        extPath=extPath/(ext['key']+"."+ext['format'])
        if ext['format']=="json":
            with open(extPath, 'r', encoding='utf-8') as f:
                instance[ext['key']]=json.load(f)
        else:
            with open(extPath, 'r', encoding='utf-8') as f:
                instance[ext['key']]=f.read()
    return instance


def loadInstance(instanceDir:Path)->dict:
    instanceDir=Path(instanceDir)
    instanceJsonPath=instanceDir/"wemuInstance.json"
    with open(instanceJsonPath, 'r', encoding='utf-8') as f:
        instance=json.load(f)
    instance=processExternalFilesLoad(instanceDir,instance)
    for key in ['rooms','worlds','characters']:
        for containedThing in instance[key]:
            instance[key]=processExternalFilesLoad(instanceDir,containedThing)
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
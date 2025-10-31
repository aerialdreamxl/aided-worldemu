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
def newRoom():#新建房间
    return {
        'version': dataVersion,         #数据版本
        'type': "room",                 #房间
        'id': "template",               #字符串id
        'name': "",                     #名字
        'simulationName': "模板",
        'desc': "",                     #描述
        'characters': [],               #次级数字人信息
        'history': [],                  #历史对话记录
        'resume': {},                   #预留项
        'externalFiles': []             #外置数据列表
    }
def newAgentCharacter():#新建数字人
    return {
        'version': dataVersion,         
        'type': "agentCharacter",       #数字人
        'id': "template",               #字符串id
        'name': "",                     #名字
        'personality': "",              #人格描述
        'modeling': "",                 #外貌描述
        'emotion': "",                  #情感
        'lastTick': 0,                  #上次调用时的Tick
        'memory': [],                   #的记忆
        'relations': {},                #的关系
        'rawChatHistory': [],           #的对话历史
        'externalFiles': []             
    }
def newInstance():
    return {
        'version': dataVersion,         
        'type': "instance",             #世界数据
        'name': "默认房间",
        'simulationName': "模板",
        'countries': [],                     #唯一的房间
        'externalFiles': []             
    }
def newWholeStructure():#新建整个实例
    room=newRoom()
    agentCharacter=newAgentCharacter()
    agentCharacter['externalFiles']=[
        { 'path': "characters/template/personality.txt", 'key': 'personality'},
        { 'path': "characters/template/modeling.txt", 'key': 'modeling'},
        { 'path': "characters/template/rawChatHistory.json", 'key': 'rawChatHistory'},
        { 'path': "characters/template/memory.json", 'key': 'memory'},
        { 'path': "characters/template/relations.json", 'key': 'relations'}
    ]
    room['characters'].append(agentCharacter)
    room['externalFiles']=[
        { 'path': "characters/characters.json", 'key': 'characters'},     
        { 'path': "rooms/room/history.json", 'key': 'history'}
    ]
    world=newInstance()
    world['countries']=[room]
    world['externalFiles']=[{ 'path': "rooms/room.json", 'key': 'room'}]
    return world

#数据保存逻辑
def saveAll(baseDir:Path, instance:dict, secretify:bool=False):
    baseDir=baseDir.resolve()
    instanceDir=Path(baseDir/instance['simulationName'])
    instanceDir.mkdir(exist_ok=True)
    instanceConfigPath=instanceDir/"wemu_config.json"

    if instance['type']=='world':
        print()
    else:
        print()

    instanceConfigPath.write_text(json.dumps(instance, ensure_ascii=False, indent=2), encoding='utf-8')

saveAll(baseDir=Path("userdata"),instance=newWholeStructure())
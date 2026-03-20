import os
import json
import re
from typing import List, Dict, Any, Optional, Tuple

ENV_PLACEHOLDER = "__FROMKEYENV__"

# 为提高兼容性，咱把所有可能的api key环境变量名全试一遍
possibleKeyEnv=["WEMU_AGENT_API_KEY","DASHSCOPE_API_KEY","OPENAI_API_KEY","ANTHROPIC_API_KEY","MODELSCOPE_API_KEY","OPENROUTER_API_KEY"]

def resolve_api_key(key: str) -> str:
    """
    解析 API Key。
    如果是占位符，从环境变量读取；否则原样返回。
    """
    if key == ENV_PLACEHOLDER:
        for keyEnv in possibleKeyEnv:
            key = os.environ.get(keyEnv,"EMPTY")
            if key != "EMPTY": break
    return key

def merge_config(world_setting: dict, entity_ai_backend: Optional[dict] = None) -> dict:
    """
    合并配置：全局 setting + 实体 aiBackend 覆盖。
    同时解析 API Key 占位符。
    
    :param world_setting: World["setting"] 字典
    :param entity_ai_backend: WAA["aiBackend"] 字典 (可选)
    :return: 合并后的完整配置字典
    """
    readyConfig = entity_ai_backend.copy()

    for i in ["baseURL","apiKey","model","modelLang","expertSettings","temperature","seed","top-p","extraBody"]:
        if readyConfig.get(i) == None:
            readyConfig[i] = world_setting["agent-api-defaults"][i]
    
    readyConfig["apiKey"] = resolve_api_key(key=readyConfig["apiKey"])
    
    return readyConfig

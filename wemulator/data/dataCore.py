# wemu-core/data/dataCore.py
import json
import uuid
from pathlib import Path

# 配置文件固定名称
CONFIG_FILENAME = "WEmulatorWorldConfig.json"
# 环境变量占位符
ENV_PLACEHOLDER = "__FROMKEYENV__"
# 世界配置类型标识
WORLD_CONFIG_TYPE = "WorldConfig"

def new(name: str = "New World", type: str = "World") -> dict:
    """
    工厂函数：新建不同类型的配置字典。
    """
    if type == "World":
        return {
            "type": WORLD_CONFIG_TYPE,# 世界配置文件的类型
            "name": name,# 世界名
            "setting": {# 系统设置
                "agent-api-defaults":{
                    "baseURL": "http://localhost:1234/v1",# OpenAI API或是未来其他什么东西的base url
                    "apiKey": ENV_PLACEHOLDER,# 你的API Key，这边建议保管好别丢了
                    "model": "qwen3.5-35b-a3b",# 默认的模型，随便你喜欢的什么模型，但建议使用Qwen系模型，因为我是在这种模型上测试的
                    "modelLang": "zhcn" # 你喜欢的模型的母语，就是开发该模型的团队或个人的母语，例如Qwen是阿里云开发的，母语是中文，llama是MetaAI开发的，母语是英文
                }
            },
            "entities": [],# 实体列表，目前只做了WAAConfig
            "unifiedRawChatHistory": {}# WAA的对话历史
        }
    
    elif type == "WAAConfig":# WAA(WEmulator Actor Agent)的配置实体
        return {
            "id": str(uuid.uuid4()),# 一个UUID，不太可能会冲突吧？
            "type": "WAAConfig",# 类型，不然你不知道这是啥
            "name": name,# 人都得有个名，对吧？
            "personality": "",# 性格
            "appearance": "",# 长相
            "aiBackend": {}# 对AI后端默认设置的某些覆写，只要你喜欢
        }
    
    else:
        raise ValueError(f"[DataCore] Not implemented: {type}")# 有些东西目前还没写好，咱得一步一个脚印慢慢来

def save(worldConfig:dict, base_dir: Path | str) -> Path:
    """
    将世界配置保存到指定目录。
    """
    base_path = Path(base_dir)
    
    if worldConfig.get("type") != WORLD_CONFIG_TYPE:
        raise ValueError(f"[DataCore] We doesn't allow save anything except a world.")# 你不会保存半个文件的，对吧？
    
    world_dir_name = worldConfig["name"]
    
    world_folder = base_path / world_dir_name
    world_folder.mkdir(parents=True, exist_ok=True)
    
    config_path = world_folder / CONFIG_FILENAME
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(worldConfig, f, ensure_ascii=False, indent=2)
        
    print(f"[DataCore] Saved: {config_path}")
    return world_folder

def load(world_dir: Path | str) -> dict:
    """
    从指定世界文件夹加载配置。
    """
    world_path = Path(world_dir)
    config_path = world_path / CONFIG_FILENAME
    
    if not config_path.exists():
        raise FileNotFoundError(f"[DataCore] File not found: {config_path}")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        world_data = json.load(f)
    
    if world_data.get("type") != WORLD_CONFIG_TYPE:
        raise ValueError(f"[DataCore] This isn't a full world configuration file.")
    
    world_data["name"] = world_path.name
            
    return world_data

def scan(base_dir: Path | str) -> list[str]:
    """
    扫描指定目录下的所有一级子文件夹，判断是否为有效的世界文件夹。
    """
    base_path = Path(base_dir)
    if not base_path.exists():
        return []
    
    world_names = []
    
    for item in base_path.iterdir():
        if item.is_dir():
            config_file = item / CONFIG_FILENAME
            if config_file.exists():
                world_names.append(item.name)
                
    return world_names
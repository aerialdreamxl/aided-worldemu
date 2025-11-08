from .openAIBackend import openAILLMGenerate
from .dashscopeBackend import dashscopeLLMGenerate

def AutoLLMGenerate(history:list,newMsg:str,config:dict)->tuple[list,str,str]:
    if config["type"]=="openai":
        return openAILLMGenerate(history,newMsg,config)
    elif config["type"]=="dashscope":
        return dashscopeLLMGenerate(history,newMsg,config)
    else:
        raise RuntimeError("LLM backend not found")

class backend:
    AutoLLMGenerate=AutoLLMGenerate,
    openAILLMGenerate=openAILLMGenerate,
    dashscopeLLMGenerate=dashscopeLLMGenerate

__all__=["backend"]
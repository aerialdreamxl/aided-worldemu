import dashscope
from http import HTTPStatus
import os

def dashscopeLLMGenerate(history:list,newMsg:str,config:dict)->tuple[list,str,str]:
    dashscope.api_key=os.environ.get("DASHSCOPE_API_KEY",config['apiKey'])
    if newMsg!="":
        history.append({'role':'user','content':newMsg})
    respond=dashscope.Generation.call(model=config['model'],messages=history,result_format="message",stream=True,incremental_output=True,enable_thinking=config['thinking'])
    aiResponce=""
    aiThinking=""
    for chunk in respond:
        if chunk.status_code==HTTPStatus.OK:
            aiResponce+=chunk.output.choices[0].message.content
            aiThinking+=chunk.output.choices[0].message.reasoning_content
    history.append({'role':'assistant','content':aiResponce})
    return history,aiResponce,aiThinking

def main():
    print("Dashscope backend testing...")
    print("Test 01: Non-thinking model")
    cfg={
        "apiKey":"you guess xd",
        "model":"qwen-flash",
        "thinking": False
    }
    history,aiResponce,aiThinking=dashscopeLLMGenerate(history=[],newMsg="随便写点什么,什么都行,长度任意,最好带几个换行",config=cfg)
    print("AI's thinking:",aiThinking)
    print("AI's responce:",aiResponce)
    print("History set:",history)
    print("Test 02: Thinking model")
    cfg["thinking"]=True
    history,aiResponce,aiThinking=dashscopeLLMGenerate(history=[],newMsg="随便写点什么,什么都行,长度任意,最好带几个换行",config=cfg)
    print("AI's thinking:",aiThinking)
    print("AI's responce:",aiResponce)
    print("History set:",history)

if __name__=="__main__":
    main()
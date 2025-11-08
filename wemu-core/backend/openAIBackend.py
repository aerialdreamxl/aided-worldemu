import openai
def openAIGenerate(history:list,newMsg:str,config:dict)->tuple[list,str,str]:
    client=openai.OpenAI(api_key=config['apiKey'],base_url=config['baseURL'])
    if newMsg!="":
        history.append({'role':'user','content':newMsg})
    respond=client.chat.completions.create(
        model=config['model'],
        messages=history,
        stream=True
    )
    aiResponce=""
    aiThinking=""
    for chunk in respond:
        aiResponce+=chunk.choices[0].delta.content
        if hasattr(chunk.choices[0].delta,"reasoning"):
            aiThinking+=chunk.choices[0].delta.reasoning
        elif hasattr(chunk.choices[0].delta,"reasoning_content"):
            aiThinking+=chunk.choices[0].delta.reasoning_content
    history.append({'role':'assistant','content':aiResponce})
    return history,aiResponce,aiThinking
def main():
    print("OpenAI backend testing...")
    print("Test 01: Non-thinking model")
    cfg={
        "apiKey":"ollama",
        "baseURL":"http://192.168.3.232:11434/v1",
        "model":"qwen3-2507-instruct:30b-q2k"
    }
    history,aiResponce,aiThinking=openAIGenerate(history=[],newMsg="随便写点什么,什么都行,长度任意,最好带几个换行",config=cfg)
    print("AI's thinking:",aiThinking)
    print("AI's responce:",aiResponce)
    print("History set:",history)
    print("Test 02: Thinking model")
    cfg["model"]="qwen3-2507-thinking:30b-q2k"
    history,aiResponce,aiThinking=openAIGenerate(history=[],newMsg="随便写点什么,什么都行,长度任意,最好带几个换行",config=cfg)
    print("AI's thinking:",aiThinking)
    print("AI's responce:",aiResponce)
    print("History set:",history)

if __name__=="__main__":
    main()
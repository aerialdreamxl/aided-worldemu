from openai import OpenAI
from .backendCommons import resolve_api_key,merge_config

def LLMGeneration(aiConfig: dict, history: list, prompt: str) -> tuple[list,str,str] :
    client = OpenAI( base_url=aiConfig["baseURL"], api_key=aiConfig["apiKey"] )
    history.append( {"role": "user", "content": prompt} )
    chatData = []
    if aiConfig["expertSettings"]:
        chatData = client.chat.completions.create(
            model=aiConfig["model"],
            messages=history,
            stream=True,
            temperature=aiConfig["temperature"],
            seed=aiConfig["seed"],
            top_p=aiConfig["top-p"],
            extra_body=aiConfig["extraBody"])
    else:
        chatData = client.chat.completions.create( model=aiConfig["model"], messages=history, stream=True )
    
    thinking=""
    response=""
    for chunk in chatData:
        delta = chunk.choices[0].delta
        if hasattr(delta, "reasoning_content"):
            thinking += delta["reasoning_content"]
        if hasattr(delta, "reasoning"):
            thinking += delta["reasoning"]
        if hasattr(delta, "thinking"):
            thinking += delta["thinking"]
        if hasattr(delta, "content"):
            response += delta["content"]
    
    history.append({"role": "assistant", "content": response})
    return history,response,thinking
import g4f

PROVIDER = {
    "gpt-3.5-turbo": g4f.Provider.Liaobots,
    "gpt-4": g4f.Provider.Liaobots,
    
}


async def query_ai(ai_title: str, query_text: str): 
    response = ''.join(await g4f.ChatCompletion.create_async(
        model=ai_title,
        provider=PROVIDER[ai_title],
        messages=[{"role": "user", "content": query_text}]
    ))
    return response

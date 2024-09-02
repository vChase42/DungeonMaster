from ollama import Client
from dotenv import load_dotenv
import os
load_dotenv()


class aiConnection:
    
    def __init__(self) -> None:
        self.url = os.getenv('CHAT_AI_URL')
        self.model = os.getenv('MODEL')
        self.client = Client(host = self.url)
        self.sysPrompt = os.getenv('SYSTEM_PROMPT')
        self.history = self.blankHistory()

        
        
    
    
    def testAiConnection(self):
        response = self.client.chat(model='gemma_abl_27b', messages=[
        {
            'role': 'user',
            'content': 'if you can read this message respond with the word yes',
        },
        ])
        if response:
            print("Connection working fine")
        else:
            print("Something is wrong")
            
    def showParams(self):
        print(f"The URL is: {self.url}")
        print(f"The model is currently: {self.model}")
        print(f"The client: {self.client}")
        print(f"The system prompt is as follows: {self.sysPrompt}")
        print(f"History: {self.history}")
    
        
    def appendHistory(self,role,message):
            self.history.append({
            'role': role,
            'content': message
        })

    def askAi(self,newMessage):
        self.appendHistory(role = 'user',message = newMessage)
        aiResponse = self.client.chat(model=self.model, messages=self.history)
        self.appendHistory(role = 'assistant',message = aiResponse)
        
    def getAiResponseAsync(self, newMessage):
        self.appendHistory(role = 'user',message = newMessage)
        aiResponse = ""
        for chunk in self.client.chat(model=self.model, messages=self.history, stream=True):
            aiResponse += chunk.get("message").get('content')
            yield f"{chunk.get("message").get('content')}"  # Proper SSE format
        self.appendHistory(role = 'assistant',message = aiResponse)
        
    def blankHistory(self):
        self.history = [{
        'role': 'system',
        'content': self.sysPrompt,
    }]

if __name__ == '__main__':
    ai = aiConnection()
    #ai.testAiConnection()
    ai.showParams()
    x= ai.askAi("tell me a joke")
    print(x)
    ai.showParams()
    y = ai.askAi("another one")
    print(y)
    ai.showParams()
    
    
   # ai.showParams()
    
        




# def ai_thing(user_input):
    # global CHAT_HISTORY
    # CHAT_HISTORY.append({
    #     'role':'user',
    #     'content': user_input
    # })
##
    # ai_response = ""
    # # Stream the API response
    # for chunk in client.chat(model='gemma_abl_27b', messages=CHAT_HISTORY, stream=True):
    #     ai_response += chunk.get("message").get('content')
    #     yield f"{chunk.get("message").get('content')}"  # Proper SSE format
    #     # print(ai_response)
    # CHAT_HISTORY.append({
    #     'role':'assistant',
    #     'content':ai_response
    #     })
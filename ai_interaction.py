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
        self.clearHistory()

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
        """appendHistory appends the message and who sent it to the running history of the chat

        Arguments:
            role -- role is either user, assistant, or system.
            message -- message to be appended to the current history
        """
        self.history.append({
        'role': role,
        'content': message
        })

    def askAi(self,newMessage):
        self.appendHistory(role = 'user',message = newMessage)
        aiResponse = self.client.chat(model=self.model, messages=self.history)
        self.appendHistory(role = 'assistant',message = aiResponse)
        return aiResponse['message']['content']
        
    def askAiOnce(self, newMessage):
        aiResponse = self.client.chat(model = self.model, messages = [{'role':'user','content':newMessage}])
        return(aiResponse['message']['content'])
        
    async def getAiResponseAsync(self, newMessage): 
        self.appendHistory(role = 'user',message = newMessage)
        aiResponse = ""
        for chunk in self.client.chat(model=self.model, messages=self.history, stream=True):
            aiResponse += chunk.get('message').get('content')
            yield f"{chunk.get('message').get('content')}"  # Proper SSE format
        self.appendHistory(role = 'assistant',message = aiResponse)
        
    def clearHistory(self): #removes all the history of the chat except the system prompt
        self.history = [{
        'role': 'system',
        'content': self.sysPrompt,
    }]
        
    def getNewButtonText(self):
        
        story_so_far = self.getStoryOnly()
        prompt = [{
            'role':'system',
            'content': os.getenv('GET_BUTTON_SYS_PROMPT')
        }]
        prompt.append({
            'role': 'user',
            'content':story_so_far + "\nGENERATE SAMEPLE ACTION 1 in TEN WORDS OR LESS:"
        })
        
        aiResponse = self.client.chat(model=self.model, messages=prompt)['message']['content']
        
        prompt[-1]['content'] = story_so_far + "\This is sample action 1: " + aiResponse + "\nGENERATE SAMPLE ACTION 2 in TEN WORDS OR LESS:"
        
        aiResponse2 = self.client.chat(model=self.model,messages=prompt)['message']['content']
        return aiResponse, aiResponse2

    
    def getStoryOnly(self):
        the_story = ""
        for x in self.history:
            if x['role'] == 'assistant':
                the_story += x['content'] + "\n"
        return the_story


if __name__ == '__main__':
    ai = aiConnection()
    ai.testAiConnection()
    ai.showParams()
    print('-------------------')
    response = ai.askAi('hello')
    print(response)
    print('-------------------')
    response = ai.askAiOnce('hi')
    print(response)
    

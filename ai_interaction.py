from ollama import Client
from dotenv import load_dotenv
import os
import json
import re
import parse_out_json
load_dotenv()


class aiConnection:

    def __init__(self) -> None:
        self.url = os.getenv('CHAT_AI_URL')
        self.model = os.getenv('MODEL')
        self.client = Client(host = self.url)
        self.sysPrompt = os.getenv('SYSTEM_PROMPT')
        self.clearHistory()
        self.tokensUsed= 0

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
    
    def getResponseDetails(self):
        self.clearHistory()
        aiResponse = self.askAiOnce('if i say yes, you say?')
        return aiResponse
    
    def askAiOnce(self, newMessage):
        aiResponse = self.client.chat(model = self.model, messages = [{'role':'user','content':newMessage}])
        return(aiResponse)
        
    async def getAiResponseAsync(self, newMessage: str): 
        #if newMessage != "begin story":
            #newMessage +=". incorporate this statement into the story."
        self.appendHistory(role = 'user',message = newMessage)
        aiResponse = ""
        for chunk in self.client.chat(model=self.model, messages=self.history, stream=True):
            aiResponse += chunk.get('message').get('content')
            yield f"{chunk.get('message').get('content')}"  # Proper SSE format
        
        self.appendHistory(role = 'assistant',message = aiResponse)
        print(f"The following is the actual story Thread: {aiResponse}")
        # with open('responseTest.json', 'a') as f:
        #     json.dump(aiResponse['eval_count'],f, indent = 6)
        #     f.close()
        
    def clearHistory(self): #removes all the history of the chat except the system prompt
        self.history = [{
        'role': 'system',
        'content': self.sysPrompt,
    }]
        
    # def getNewButtonText(self):
        
    #     story_so_far = self.getStoryOnly()
    #     prompt = [{
    #         'role':'system',
    #         'content': os.getenv('GET_BUTTON_SYS_PROMPT')
    #     }]
    #     prompt.append({
    #         'role': 'user',
    #         'content':story_so_far + "\nGENERATE SAMEPLE ACTION 1 in TEN WORDS OR LESS:"
    #     })
        
    #     aiResponse = self.client.chat(model=self.model, messages=prompt)['message']['content']
        
    #     prompt[-1]['content'] = story_so_far + "\This is sample action 1: " + aiResponse + "\nGENERATE SAMPLE ACTION 2 in TEN WORDS OR LESS:"
        
    #     aiResponse2 = self.client.chat(model=self.model,messages=prompt)['message']['content']
    #     return aiResponse, aiResponse2
    
    def getStoryOnly(self):
        the_story = ""
        for x in self.history:
            if x['role'] == 'assistant':
                the_story += x['content'] + "\n"
        return the_story
    
    def convertFromJsonToDict(self,string):
        return parse_out_json.getDict(string)
    
    def changeSysPrompt(self, newSysPrompt = 'GEN_BUTTON_SYS_PROMPT'):
        newPrompt = [{
            'role':'system',
            'content':os.getenv(newSysPrompt)
        }]
        return newPrompt
    #def 
        
    def generateOptions(self):
        newPrompt = self.changeSysPrompt()
        #print(f"This is the newPrompt:\n{newPrompt}")
        storySoFar = self.getStoryOnly()
        #print(f"This is the story_so_far:\n{storySoFar}")
        newPrompt.append({
            'role':'user',
            'content':storySoFar + '''\nbased on the story so far, provide two actions that are relevant to continue the story. provide only the answer as json, nothing else, with 
                keys as the option numbers and values as the actual options exactly like this: {"option1": "jim fires the gun", "option2":"jim runs away"}'''
        })
        aiResponse = self.client.chat(model=self.model, messages=newPrompt)#['message']['content']
        #print(f"This is the story so far:\n{storySoFar}")
        self.tokensUsed = aiResponse['eval_count'] #have not tested this out fully yet.
        print(f"Current tokens used: {self.tokensUsed}")
        #aiResponseDict = self.convertFromJsonToDict(aiResponse)
        print(f"Current history:\n{self.history}")
        return self.convertFromJsonToDict(aiResponse['message']['content'])
        
        
    
    def getNewButtonText(self):
        
        # story_so_far = self.getStoryOnly()
        # prompt = [{
        #     'role':'system',
        #     'content': os.getenv('GET_BUTTON_SYS_PROMPT')
        # }]
        # prompt.append({
        #     'role': 'user',
        #     'content':story_so_far + "\nGENERATE SAMEPLE ACTION 1 in TEN WORDS OR LESS:"
        # })
        
        ####below is working
        # prompt=self.history.copy()
        # prompt.append({
        #     'role': 'user',
        #     'content':'''based on the story so far, provide two actions that are relevant to continue the story. provide only the answer as json, nothing else, with 
        #         keys as the option numbers and values as the actual options exactly like this: {"option1": "jim fires the gun", "option2":"jim runs away"}'''
        # })
        # #print(len(prompt))
        # #print(len(self.history))
        # aiResponse = self.client.chat(model=self.model, messages=prompt)['message']['content']
        # print(aiResponse)
        
        #####end working
        #matches = re.findall(r'\{.*?\}', aiResponse)
        #aiResponseDict = json.loads(matches[0])

        #prompt[-1]['content'] = story_so_far + "\This is sample action 1: " + aiResponse + "\nGENERATE SAMPLE ACTION 2 in TEN WORDS OR LESS:"
        
        #aiResponse2 = self.client.chat(model=self.model,messages=prompt)['message']['content']
        aiResponseDict = self.generateOptions()
        print(f'These are the options that should be displayed:\n{aiResponseDict}')
        return aiResponseDict['option1'], aiResponseDict['option2']
    
    
    def recordTokens(self):
        pass

if __name__ == '__main__':
    ai = aiConnection()
    #ai.testAiConnection()
    #ai.showParams()
    #print('-------------------')
    #response = ai.askAi('hello')
    #print(response)
    #print('-------------------')
    #response = ai.askAiOnce('hi')
    #print(response)
    response = ai.getResponseDetails()
    #print(response)
    #jsonResponse = json.dump(response)
    with open('responseTest.json', 'w') as f:
        json.dump(response['eval_count'],f, indent = 6)
        f.close()
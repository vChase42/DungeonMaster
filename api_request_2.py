from ollama import Client
import json
import re
client = Client(host='http://192.168.1.11:11434')
response = client.chat(model='gemma_abl_27b', messages=[
  {
    'role': 'user',
    'content': '''based on the story so far, provide two actions that are relevant to continue the story. provide only the answer as json, nothing else, with 
                keys as the option numbers and values as the actual options exactly like this: {"option1": "jim fires the gun", "option2":"jim runs away"}''',

  },
])
responseText = response.get('message').get('content')
print(responseText)
matches = re.findall(r'\{.*?\}', responseText)
json_dict = json.loads(matches[0])

print (json_dict)






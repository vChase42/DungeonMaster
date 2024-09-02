from ollama import Client
client = Client(host='http://192.168.1.11:11434')
response = client.chat(model='gemma_abl_27b', messages=[
  {
    'role': 'user',
    'content': 'whats the largest number you know. If there isnt a specific limit, just print a large ass number',
  },
])


print(response.get("message").get('content'))



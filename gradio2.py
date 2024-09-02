import gradio as gr
from ollama import Client

# Initialize the client
client = Client(host='http://192.168.1.11:11434')

CHAT_HISTORY = []
prompt_1 = "Take me on a scifi thriller adventure"
prompt_2 = "Tell me on a crazy adventure that starts out in a mideval castle"

# Function to handle chat response with streaming
def respond_to_input(chat_window, user_input, prompt=None):
    global CHAT_HISTORY, prompt_1, prompt_2
    if prompt:
        if prompt == "1":
            user_input = prompt_1
        elif prompt == "2":
            user_input = prompt_2
    

    # Add user input to chat history
    chat_window.append((user_input, ""))
    CHAT_HISTORY.append({
            'role': 'user',
            'content': user_input,
        })
    
    # Initialize a placeholder for the AI response
    
    ai_response = ""
    # Stream the API response
    for chunk in client.chat(model='gemma_abl_27b', messages=CHAT_HISTORY, stream=True):
        ai_response += chunk.get("message").get('content')
        chat_window[-1] = (user_input, ai_response)
        yield chat_window, gr.update(value=""), gr.Button(prompt_1), gr.Button(prompt_2)
    
    
    CHAT_HISTORY.append({
            'role': 'assistant',
            'content': ai_response,
        })
    prompt_1 = generate_response(ai_response + "\nBased on the story, generate 1 prompt that is 10 words or less that the audience might be curious about. Only state the prompt, nothing else.")
    prompt_2 = generate_response(ai_response + "\nBased on the story, generate a crazy prompt that is 10 words or less to help that the audience might be curious about. Only state the prompt, nothing else. Make it different from this prompt: " + prompt_1)

    #UPDATE BUTTON1 and BUTTON2 HERE with PROMPT_1 and PROMPT_2
    # print(prompt_1,prompt_2)
    yield chat_window, gr.update(value=""), gr.Button(prompt_1), gr.Button(prompt_2)


def generate_response(prompt):
    new_chat = [{
        'role':'system',
        'content': "You are responsible for providing a sentence for the next possible action that a user may take for this story." 
    },
    {
        'role': 'user',
        'content': prompt
    }]

    response = client.chat(model='gemma_abl_27b', messages=new_chat)
    return response.get("message").get('content')


inventory = {}
def update_inventory(key,value):
    global inventory
    inventory[key] = value
    pass
def get_inventory():
    global inventory
    return inventory.to_string()


# Predefined prompts
# Define UI components
with gr.Blocks() as demo:
    chat_window = gr.Chatbot(label="Chat History", elem_id="chatbox")
    
    with gr.Row():
        button1 = gr.Button(prompt_1)
        button2 = gr.Button(prompt_2)
    
    user_input = gr.Textbox(placeholder="Type your custom prompt here...", label="Custom Prompt")
    

    # Events
    button1.click(respond_to_input, inputs=[chat_window, user_input, gr.State("1")], outputs=[chat_window, user_input,button1,button2])
    button2.click(respond_to_input, inputs=[chat_window, user_input, gr.State("2")], outputs=[chat_window, user_input,button1,button2])
    user_input.submit(respond_to_input, inputs=[chat_window, user_input, gr.State(None)], outputs=[chat_window, user_input,button1,button2])




inventory_rules = "The user has an inventory, which will be maintained with a python dictionary. You will receive the hero inventory with every prompt. you may update the inventory with {UPDATEINVENTORY: KEY:VALUE}"
CHAT_PREPROMPT = "You will tell one story at a time. You will keep track of the state of the world, and be as realistic as possible. The world is as unexpected as it is boring! Whenever a new character or creature is introduced, brainstorm that entities stats/weaknesses/strengths/personality inside of a <>. You do not need to fill every field. If the hero states an unsusual, nonsensical request that is irrelevant to the story, ask the hero if they're sure." + inventory_rules

# CHAT_HISTORY = "You are a timeless story teller, who is unparalleled in your ability to tell engaging stories and incorporate your audiences ideas into your stories. Keep your story chunks to 1 page. The audience give you a prompt to get you started."
SYSTEM_PROMPT = "You are a dungeon master. You will lead the hero on a journey of his choosing. You will tell a story 1 page at a time. You will keep track of the state of the world, and be as realistic as possible. The world is as unexpected as it is boring! Whenever a new character or creature is introduced, brainstorm that entities stats/weaknesses/strengths/personality inside of a <>. You do not need to fill every field. DO NOT PROVIDE ME WITH OPTIONS, USER WILL PROVIDE THEM."
CHAT_HISTORY.append({
    'role': 'system',
    'content': SYSTEM_PROMPT,
})



if __name__ == "__main__":
    # Launch the app
    demo.launch()


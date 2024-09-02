# app.py
from flask import Flask, Response, render_template, request, redirect, url_for
from ollama import Client
# from flask_socketio import SocketIO, emit

from ai_interaction import aiConnection


# Initialize the client
client = Client(host='http://192.168.1.11:11434')

AI_CONNECTION = aiConnection()
# CHAT_HISTORY = []
# SYSTEM_PROMPT = "You are a dungeon master. You will lead the hero on a journey of his choosing. You will tell a story 1 page at a time. You will keep track of the state of the world, and be as realistic as possible. The world is as unexpected as it is boring! Whenever a new character or creature is introduced, brainstorm that entities stats/weaknesses/strengths/personality inside of a <>. You do not need to fill every field. DO NOT PROVIDE ME WITH OPTIONS, USER WILL PROVIDE THEM."

# CHAT_HISTORY.append({
#     'role': 'system',
#     'content': SYSTEM_PROMPT,
# })

app = Flask(__name__)
# socketio = SocketIO(app)
button1_label = "Button 1"
button2_label = "Button 2"

@app.route('/', methods=['GET'])
def index():
        
    return render_template('index.html',
                           button1_label=button1_label, 
                           button2_label=button2_label)

@app.route('/clear',methods=['POST'])
def clear_history():
    AI_CONNECTION.blankHistory()
    return redirect(url_for('index'))


# @socketio.on('text_update')
# async def handle_text_update(textfield_content):
#     async for chunk in AI_CONNECTION.getAiResponseAsync(textfield_content):
#         print("chunk")
#         emit('broadcast_ai_response', {'ai_response_chunk': chunk}, broadcast=True)



@app.route('/submit',methods=['POST'])
def query_submitted():
    # print("potato")
    # textfield_content = request.form.get('text_field')
    # socketio.start_background_task(handle_text_update, {'textfield_content': textfield_content})
    # return "this"
    # handle_text_update(textfield_content)
    textfield_content = request.form.get('user_input')
    print(textfield_content)

    return Response(AI_CONNECTION.getAiResponseAsync(textfield_content))




if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5000)





    # text_field_content = request.form.get('text_field')
    # button_clicked = request.form.get('button')

    # global button1_label, button2_label
    # button1_label = "potato"
    # button2_label = "potato2"
    # # Handle the data (print to console, process, save, etc.)
    # print(f"Large Textbox: {large_textbox_content}")
    # print(f"Text Field: {text_field_content}")
    # print(f"Button Clicked: {button_clicked}")

    # Optionally, redirect or render a template with the data

    # return redirect(url_for('index'))
    # return render_template('index.html', 
    #                         button1_label="potato",
    #                         button2_label="potato2")

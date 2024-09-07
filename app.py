# app.py
import os
from ollama import Client
from dotenv import load_dotenv
from flask import Flask, Response, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
# import eventlet
import asyncio

load_dotenv()
from ai_interaction import aiConnection

# Initialize the client
client = Client(host=os.getenv('CHAT_AI_URL'))
#ser

AI_CONNECTION = aiConnection()

# eventlet.monkey_patch()
app = Flask(__name__)
socketio = SocketIO(app)


button1_label = "Tell me a story about scientists and witches"
button2_label = "Tell me a fantasy story"

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html',
                           button1_label=button1_label, 
                           button2_label=button2_label)

@app.route('/clear',methods=['POST'])
def clear_history():
    AI_CONNECTION.clearHistory()
    return redirect(url_for('index'))


@socketio.on('text_update')
def handle_text_update(textfield_content):
    print("received a query from user")
    asyncio.run(ai_response(textfield_content))

async def ai_response(textfield_content):
    async for chunk in AI_CONNECTION.getAiResponseAsync(textfield_content):
        emit('broadcast_ai_response', {'ai_response_chunk': chunk}, broadcast=True)

    buttonText1, buttonText2 = AI_CONNECTION.getNewButtonText()
    emit('update_buttons',(buttonText1, buttonText2))



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
    socketio.run(app,debug=True,host="0.0.0.0",port=5000)





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

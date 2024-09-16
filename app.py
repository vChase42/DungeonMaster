# app.py
import os
from dotenv import load_dotenv
from flask import Flask, Response, jsonify, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
import asyncio

load_dotenv()
from ai_interaction import aiConnection


AI_CONNECTION = aiConnection()

app = Flask(__name__)
socketio = SocketIO(app)

is_generating = False


button1_label = "Tell me a story about scientists and witches"
button2_label = "Tell me a fantasy story"
button3_label = "Tell me a spooky story"
button4_label = "Tell me a 21st century dystopia story"

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html',
                           textarea_story = AI_CONNECTION.getStoryOnly(),
                           button1_label=button1_label, 
                           button2_label=button2_label, 
                           button3_label=button3_label, 
                           button4_label=button4_label)

@app.route('/clear',methods=['POST'])
def clear_history():
    AI_CONNECTION.clearHistory()
    return redirect(url_for('index'))

@app.route('/is_generating',methods=['GET'])
def getIsGenerating():
    global is_generating
    return jsonify({'is_generating':is_generating})
        

@socketio.on('text_update')
def handle_text_update(textfield_content):
    global is_generating
    if is_generating:
        print("Ai is already generating a chunk of the story! ignoring request")
        return
    print("received a query from user")
    asyncio.run(ai_response(textfield_content))

async def ai_response(textfield_content):
    global is_generating
    is_generating = True
    async for chunk in AI_CONNECTION.getAiResponseAsync(textfield_content):
        emit('broadcast_ai_response', {'ai_response_chunk': chunk}, broadcast=True)

    buttonText1 = AI_CONNECTION.getNewButtonText("Neutral")
    buttonText2 = AI_CONNECTION.getNewButtonText("Angry")
    buttonText3 = AI_CONNECTION.getNewButtonText("Passive Aggressive")
    buttonText4 = AI_CONNECTION.getNewButtonText("Agreeable")
    emit('update_buttons',(buttonText1, buttonText2, buttonText3, buttonText4))
    global button1_label,button2_label, button3_label, button4_label
    button1_label = buttonText1
    button2_label = buttonText2
    button3_label = buttonText3
    button4_label = buttonText4

    is_generating = False



if __name__ == '__main__':
    socketio.run(app,debug=True,host="0.0.0.0",port=5000)


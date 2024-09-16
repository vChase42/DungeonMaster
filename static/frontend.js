console.log("frontend js loaded")


var socket = io.connect('http://' + document.domain + ':' + location.port);

const textarea = document.getElementById('chat-window');

socket.on('connect', function() {
    console.log('Successfully connected to the server!');
    // You can also perform any action after connection
});
socket.on('connect_error', function(error) {
    console.log('Connection failed:', error);
});


socket.on('broadcast_ai_response', function(data) {
    // console.log('Response from server:', data);
    
    textarea.value += data.ai_response_chunk
});

socket.on('update_buttons',function(button1,button2){
    const html_button1 = document.getElementById('button1');
    const html_button2 = document.getElementById('button2');
    const html_button3 = document.getElementById('button3');
    const html_button4 = document.getElementById('button4');
    
    html_button1.innerHTML = button1
    html_button2.innerHTML = button2
    html_button3.innerHTML = button3
    html_button4.innerHTML = button4
    document.getElementById('text_field').value = "";
});

async function startStreamingIO(event){
    event.preventDefault();
    console.log("button clicked");
    

    const response = await fetch('/is_generating');
    const data = await response.json();
    
    if (data.is_generating) {
        console.log("Text is already being generated! Not sending query.");
        return;  
    }

    const textarea = document.getElementById('chat-window');
    textarea.value += "-------------------------------------------------\n";  // Clear the textarea
    
    let user_input = document.getElementById('text_field').value;
    const clickedButton = event.submitter.id;
    if(user_input == ""){
        user_input = document.getElementById(clickedButton).innerHTML;
    }
    socket.emit('text_update', user_input);  // Send the message to the server


}
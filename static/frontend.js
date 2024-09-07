console.log("frontend js loaded")

function startStreaming(event) {
    event.preventDefault();  // Prevent the form from submitting traditionally

    const clickedButton = event.submitter.id;
    const textarea = document.getElementById('chat-window');
    textarea.value += "-------------------------------------------------\n";  // Clear the textarea

    const user_input = document.getElementById('text_field').value;
    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'user_input': user_input,
            'button_clicked':clickedButton
        })
    })
    .then(response => {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        function readStream() {
            reader.read().then(({ done, value }) => {
                if (done) {
                    console.log('Stream complete');
                    return;
                }
                const chunk = decoder.decode(value, { stream: true });
                textarea.value += chunk;  // Append received data to the textarea
                readStream();  // Continue reading the stream
            });
        }
        readStream();  // Start reading the stream
    })
    .catch(error => {
        console.error('Fetch error:', error);
    });    
}

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
    console.log('Response from server:', data);
    
    textarea.value += data.ai_response_chunk
});

socket.on('update_buttons',function(button1,button2){
    console.log(button1)
    const html_button1 = document.getElementById('button1');
    const html_button2 = document.getElementById('button2');

    html_button1.innerHTML = button1
    html_button2.innerHTML = button2
});

function startStreamingIO(event){
    event.preventDefault();
    console.log("button clicked");
    
    
    const textarea = document.getElementById('chat-window');
    textarea.value += "-------------------------------------------------\n";  // Clear the textarea
    
    let user_input = document.getElementById('text_field').value;
    const clickedButton = event.submitter.id;
    if(user_input == ""){
        user_input = document.getElementById(clickedButton).innerHTML;
    }
    socket.emit('text_update', user_input);  // Send the message to the server


}
async function sendMessage() {
    let userInput = document.getElementById("user-input").value;
    if (!userInput) return;

    let chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `<p class="user-message"><strong>You:</strong> ${userInput}</p>`;

    document.getElementById("user-input").value = ""; // Clear input box

    // Send request to backend
    try{
    let response = await fetch("http://127.0.0.1:5500/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: userInput })
    });

    let data = await response.json();   
    

    chatBox.innerHTML += `<p class="bot-message"><strong>AI:</strong> ${data.response}</p>`;

    // Auto-scroll to latest message
    chatBox.scrollTop = chatBox.scrollHeight;
}catch(err){
    console.log(err.message)
}
}

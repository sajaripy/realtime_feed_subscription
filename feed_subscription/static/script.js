var button = document.getElementById("subscribe");
var button2 = document.getElementById("unsubscribe");


const socket = new WebSocket('wss://dstream.binance.com/stream?streams=btcusd_perp@bookTicker'); // Replace with your WebSocket URL

// Event listener for when the WebSocket connection is established
socket.onopen = function(event) {
 console.log('WebSocket connection established.');
};

// Event listener for receiving messages from the WebSocket server
socket.onmessage = function(event) {
 const data = JSON.parse(event.data);
 console.log('Received data:', data);

 // Update HTML content with live feed data
 const liveFeedContainer = document.getElementById('live-feed-container');
 const feedData = JSON.stringify(data, null, 2); // Convert data to formatted JSON string
 liveFeedContainer.innerHTML += '<pre>' + feedData + '</pre>';
};

// Event listener for WebSocket connection close
socket.onclose = function(event) {
 console.log('WebSocket connection closed.');
};

button.addEventListener("click", socket.onmessage);
button2.addEventListener("click", socket.onclose);
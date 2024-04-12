# # Import necessary libraries
# import websocket
# import json
# from .consumers import FeedConsumer


# # Binance WebSocket API URL for subscribing to live feed updates
# binance_ws_url = "wss://dstream.binance.com/stream?streams=btcusd_perp@bookTicker"

# # Define a function to handle WebSocket messages
# def on_message(ws, message):
#     # Parse the received message
#     data = json.loads(message)
    
#     # Extract relevant data from the message
#     feed_data = data['data']

#     # Send the feed data to the REST API for distribution
#     FeedConsumer.send_feed_update(feed_data)

# # Define a function to handle WebSocket errors
# def on_error(ws, error):
#     print(error)

# # Define a function to handle WebSocket connection close
# def on_close(ws):
#     print("### closed ###")

# # Define a function to handle WebSocket connection open
# def on_open(ws):
#     print("### connected ###")

#     # Subscribe to the Binance WebSocket feed
#     ws.send(json.dumps({
#         "method": "SUBSCRIBE",
#         "params": ["btcusd_perp@bookTicker"],
#         "id": 1
#     }))

# # Function to establish WebSocket connection to Binance API
# def start_binance_websocket():
#     # Create a WebSocket connection to the Binance WebSocket API
#     ws = websocket.WebSocketApp(binance_ws_url,
#                                 on_message=on_message,
#                                 on_error=on_error,
#                                 on_close=on_close)
#     ws.on_open = on_open

#     # Start the WebSocket connection
#     ws.run_forever()
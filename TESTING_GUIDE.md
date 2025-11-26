# Testing Feature 1 - Broadcast Communication

## Step 1: Start the Server
Open a terminal and run:
```
python networkfinal/server.py
```
You should see: "Server is listening on port 12000"

## Step 2: Start Multiple Clients
Open **at least 2 additional terminal windows** and in each one run:
```
python networkfinal/client.py
```

## Step 3: Test Broadcasting
- Type a message in Client 1 (e.g., "Hello everyone!")
- Press Enter
- You should see "Received: Hello everyone!" in Client 2, Client 3, etc.
- Messages from Client 2 will appear in Client 1 and Client 3
- And so on...

## Expected Behavior:
- ✅ Messages sent from one client appear in ALL other connected clients
- ✅ The sender does NOT see their own message echoed back
- ✅ Server console shows all messages being received and forwarded

## Troubleshooting:
- If you don't see "Received:" messages, make sure:
  1. Server is running first
  2. Multiple clients are connected
  3. You're typing in a different client than where you expect to see the message


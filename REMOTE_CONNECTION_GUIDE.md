# Connecting Server and Client on Different Computers

## Server Setup (No changes needed!)
The server is already configured to accept connections from other computers. Just run:
```bash
python server.py
```

## Client Setup

### Step 1: Find the Server's IP Address
On the **server computer**, run:
```bash
ipconfig
```
Look for "IPv4 Address" (e.g., `192.168.1.100`)

### Step 2: Update Client Code
On the **client computer**, change line 19 in `client.py`:
```python
serverAdd="127.0.0.1"  # Change this to the server's IP address
```
To:
```python
serverAdd="192.168.1.100"  # Replace with actual server IP
```

### Step 3: Firewall Configuration
**On the server computer**, you may need to:
- Allow Python through Windows Firewall
- Or open port 12000 in Windows Firewall

**Windows Firewall:**
1. Open Windows Defender Firewall
2. Click "Advanced settings"
3. Click "Inbound Rules" → "New Rule"
4. Select "Port" → Next
5. Select "TCP" and enter port "12000"
6. Allow the connection
7. Apply to all profiles

### Step 4: Test Connection
1. Start server on Computer A
2. Update client.py with Computer A's IP address
3. Run client.py on Computer B
4. They should connect!

## Example:
- **Server Computer IP:** `192.168.1.100`
- **Client Computer:** Change `serverAdd="192.168.1.100"` in client.py

## Troubleshooting:
- **Connection refused:** Check firewall settings on server
- **Can't find server:** Make sure both computers are on the same network
- **Still not working:** Try pinging the server IP from the client computer first


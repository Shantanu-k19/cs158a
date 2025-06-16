# Variable-Length Message TCP Client-Server

This assignment implements a TCP client-server communication system that handles variable-length messages. The client sends a message with a length prefix, and the server responds by converting the specified number of characters to uppercase.

## Files
- `myvlclient.py`: Client program that sends messages to the server
- `myvlserver.py`: Server program that receives messages and converts them to uppercase

## Message Format
- First 2 bytes of the message indicate the length of the text
- Followed by the actual message text
- Example: "08shantanu" where "08" is the length and "shantanu" is the message

## How to Run

1. First, start the server:
```bash
python myvlserver.py
```

2. Then, in a separate terminal, start the client:
```bash
python myvlclient.py
```

## Execution Example

### Terminal 1 (Server):
```
PS E:\Computer Networks\cs158a> python myvlserver.py
The server is ready to receive
Connected from 127.0.0.1
msg_len: 8
processed: shantanu
msg_len_sent: 8
Connection closed
```

### Terminal 2 (Client):
```
PS E:\Computer Networks\cs158a> python myvlclient.py
Input lowercase sentence:08shantanu
From Server: SHANTANU
```

## Features
- TCP socket communication
- Variable-length message handling
- Length prefix in first 2 bytes
- Server converts specified number of characters to uppercase
- Server continues running until manually terminated (Ctrl+C)
- Client terminates after receiving the response

## Notes
- The server must be started before the client
- The length prefix must be exactly 2 bytes
- The server will only capitalize the exact number of characters specified in the length prefix
- All characters must be between UTF8 U+0000 and U+007F
- The server uses a buffer size of 64 bytes for send and receive operations

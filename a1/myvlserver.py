from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('The server is ready to receive')

while True:
    connectionSocket, addr = serverSocket.accept()
    print(f'Connected from {addr[0]}')
    
    try:
        # Receive the message
        received_data = b''
        while True:
            chunk = connectionSocket.recv(64)
            if not chunk:
                break
            received_data += chunk
            if len(received_data) >= 2:  # We have at least the length prefix
                break
        
        # Process the received message
        full_message = received_data.decode()
        
        # Extract length and message
        msg_len = int(full_message[:2])  # First 2 characters are the length
        message = full_message[2:2+msg_len]  # Get exactly msg_len characters after the length prefix
        
        print(f'msg_len: {msg_len}')
        print(f'processed: {message}')
        
        # Convert to uppercase and send back
        modifiedMessage = message.upper()
        connectionSocket.send(modifiedMessage.encode())
        print(f'msg_len_sent: {len(modifiedMessage)}')
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connectionSocket.close()
        print('Connection closed')

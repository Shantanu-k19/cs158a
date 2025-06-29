from socket import *

serverName = 'localhost'  # Change this to the server's IP address
serverPort = 12000

try:
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))

    # Get user input
    message = input('Input lowercase sentence:')

    # Send the message (including length prefix)
    clientSocket.send(message.encode())

    # Receive the response
    received_data = b''
    while True:
        chunk = clientSocket.recv(64)
        if not chunk:
            break
        received_data += chunk
        if len(received_data) >= len(message[2:]):  # We've received the expected length
            break

    # Print the received message
    print('From Server:', received_data.decode())

except Exception as e:
    print(f"Error: {e}")
finally:
    clientSocket.close()

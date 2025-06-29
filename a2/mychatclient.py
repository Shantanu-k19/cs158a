from socket import *
import threading

# Function to receive messages from the server
def receive_messages(clientSocket):
    while True:
        try:
            message = clientSocket.recv(1024).decode()
            if message:
                print(message)
            else:
                break
        except:
            break

# Main client setup
serverName = '127.0.0.1'
serverPort = 12345
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

print("Connected to chat server. Type 'exit' to leave.")

# Start a thread to receive messages
receive_thread = threading.Thread(target=receive_messages, args=(clientSocket,))
receive_thread.start()

# Send messages to the server
while True:
    message = input()
    if message.lower() == 'exit':
        clientSocket.send(message.encode())
        break
    clientSocket.send(message.encode())

clientSocket.close()
print('Disconnected from server') 
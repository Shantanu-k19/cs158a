from socket import *
import threading

# List to keep track of connected clients
clients = []

# Function to handle client connections
def handle_client(connectionSocket, addr):
    global clients
    print(f'New connection from {addr}')
    clients.append(connectionSocket)
    try:
        while True:
            # Receive message from client
            message = connectionSocket.recv(1024).decode()
            if message.lower() == 'exit':
                print(f'Client {addr} disconnected')
                clients.remove(connectionSocket)
                break
            # Print the message from the client
            print(f'{addr[1]}: {message}')
            # Relay message to all other clients
            for client in clients:
                if client != connectionSocket:
                    client.send(f'{addr[1]}: {message}'.encode())
                    
    except Exception as e:
        print(f'Error: {e}')
    finally:
        connectionSocket.close()

# Main server setup
serverPort = 12345
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen()
print('Server listening on 127.0.0.1:12345')

# Accept new client connections
while True:
    connectionSocket, addr = serverSocket.accept()
    client_thread = threading.Thread(target=handle_client, args=(connectionSocket, addr))
    client_thread.start() 
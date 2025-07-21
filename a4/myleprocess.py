import uuid
import socket
import threading
import json
import time
import sys
from queue import Queue, Empty

# Initialize a lock for logging
log_lock = threading.Lock()

# Events for synchronization
server_ready = threading.Event()
client_connected = threading.Event()

# Shared state
global leader_id, state
leader_id = None
state = 0  # 0: finding leader, 1: leader known

# Queue for messages to forward
message_queue = Queue()

class Message:
    def __init__(self, uuid, flag=0):
        self.uuid = uuid
        self.flag = flag

    def to_json(self):
        return json.dumps({'uuid': str(self.uuid), 'flag': self.flag})

    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        return Message(uuid.UUID(data['uuid']), data['flag'])

def server_function(server_ip, server_port, process_uuid, log_file):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(1)
    print(f"Server listening on {server_ip}:{server_port}")
    server_ready.set()

    conn, addr = server_socket.accept()
    handle_client(conn, process_uuid, log_file)

def handle_client(conn, process_uuid, log_file):
    global leader_id, state
    start_time = time.time()
    timeout = 60

    while True:
        if time.time() - start_time > timeout:
            print("Timeout reached, terminating process.")
            break

        data = conn.recv(1024)
        if not data:
            break

        message = Message.from_json(data.decode())
        log_received_message(message, process_uuid, log_file, state, leader_id)

        if message.flag == 0:
            if message.uuid == process_uuid:
                print(f"Leader is {process_uuid}")
                leader_id = process_uuid
                state = 1
                message.flag = 1
                message_queue.put(message)
            elif message.uuid > process_uuid:
                message_queue.put(message)
            else:
                log_ignored_message(message, log_file)

        elif message.flag == 1:
            if state == 0:
                leader_id = message.uuid
                state = 1
                print(f"Leader is {leader_id}")
                message_queue.put(message)

    conn.close()

def client_function(client_ip, client_port, process_uuid, log_file):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected = False

    while not connected:
        try:
            client_socket.connect((client_ip, client_port))
            connected = True
            client_connected.set()
        except ConnectionRefusedError:
            print(f"Connection to {client_ip}:{client_port} refused. Retrying in 5 seconds...")
            time.sleep(5)

    print(f"Connected to server at {client_ip}:{client_port}")
    server_ready.wait()
    client_connected.wait()

    initial_message = Message(process_uuid)
    client_socket.send(initial_message.to_json().encode())
    log_sent_message(initial_message, log_file)

    while True:
        if state == 1:
            break
        try:
            message = message_queue.get(timeout=1)
            client_socket.send(message.to_json().encode())
            log_sent_message(message, log_file)
        except Empty:
            continue

    client_socket.close()

def log_received_message(message, process_uuid, log_file, state, leader_id):
    with log_lock:
        with open(log_file, 'a') as f:
            comparison = "greater" if message.uuid > process_uuid else "less" if message.uuid < process_uuid else "same"
            leader_info = f", leader_id={leader_id}" if state == 1 else ""
            f.write(f"Received: uuid={message.uuid}, flag={message.flag}, {comparison}, {state}{leader_info}\n")

def log_sent_message(message, log_file):
    with log_lock:
        with open(log_file, 'a') as f:
            f.write(f"Sent: uuid={message.uuid}, flag={message.flag}\n")

def log_ignored_message(message, log_file):
    with log_lock:
        with open(log_file, 'a') as f:
            f.write(f"Ignored message: uuid={message.uuid}, flag={message.flag}\n")

def main():
    config_file = sys.argv[1] if len(sys.argv) > 1 else 'config.txt'
    with open(config_file, 'r') as f:
        lines = f.readlines()
        server_ip, server_port = lines[0].strip().split(',')
        client_ip, client_port = lines[1].strip().split(',')

    process_uuid = uuid.uuid4()
    print(f"Process UUID: {process_uuid}")
    # log_file = f"log{process_uuid.int % 3 + 1}.txt"
       # Assign log file based on config file name
    if config_file.startswith("config") and config_file.endswith(".txt"):
        log_file = f"log{config_file[6:-4]}.txt"
    else:
        log_file = "log.txt"
    server_thread = threading.Thread(target=server_function, args=(server_ip, int(server_port), process_uuid, log_file))
    client_thread = threading.Thread(target=client_function, args=(client_ip, int(client_port), process_uuid, log_file))

    server_thread.start()
    client_thread.start()

    server_thread.join()
    client_thread.join()

if __name__ == "__main__":
    main()
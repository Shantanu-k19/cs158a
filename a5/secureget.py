import socket
import ssl

HOST = 'www.google.com'
PORT = 443
REQUEST = f"""GET / HTTP/1.1\r\nHost: {HOST}\r\nConnection: close\r\nUser-Agent: SecureGet/1.0\r\nAccept: */*\r\n\r\n"""

context = ssl.create_default_context()

with socket.create_connection((HOST, PORT)) as sock:
    with context.wrap_socket(sock, server_hostname=HOST) as ssock:
        ssock.sendall(REQUEST.encode('utf-8'))
        response = b""
        while True:
            data = ssock.recv(4096)
            if not data:
                break
            response += data

# Split headers and body
header_end = response.find(b"\r\n\r\n")
if header_end != -1:
    body = response[header_end+4:]
else:
    body = response

with open("response.html", "wb") as f:
    f.write(body)

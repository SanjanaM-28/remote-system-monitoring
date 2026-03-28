import socket
import json
import time
import psutil
import platform
from cryptography.fernet import Fernet

key = b'5nG7y7r2rXQ9w1gZ9v8k3Jc9Z3k9mTzR5s6Xc7Yh8KQ='
cipher = Fernet(key)

SERVER_IP = "10.30.202.227"
PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

node_name = platform.node()

while True:
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    data = {
        "node": node_name,
        "cpu": cpu,
        "memory": memory,
        "disk": disk
    }

    json_data = json.dumps(data)
    encrypted = cipher.encrypt(json_data.encode())

    sock.sendto(encrypted, (SERVER_IP, PORT))

    print("📤 Sent:", data)

    time.sleep(5)

import socket
import json
from cryptography.fernet import Fernet

# 🔐 SAME KEY must be used in client
key = b'5nG7y7r2rXQ9w1gZ9v8k3Jc9Z3k9mTzR5s6Xc7Yh8KQ='
cipher = Fernet(key)

SERVER_IP = "0.0.0.0"
PORT = 9999

# 🚨 Thresholds
CPU_THRESHOLD = 80
MEM_THRESHOLD = 80
DISK_THRESHOLD = 90

# 📡 Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, PORT))

print("🚀 Server running on port", PORT)

while True:
    data, addr = sock.recvfrom(4096)

    try:
        # 🔓 Decrypt data
        decrypted = cipher.decrypt(data).decode()

        # 📦 Parse JSON
        metrics = json.loads(decrypted)

        node = metrics["node"]
        cpu = metrics["cpu"]
        mem = metrics["memory"]
        disk = metrics["disk"]

        print(f"\n📡 From {node} ({addr})")
        print(f"CPU: {cpu}% | Memory: {mem}% | Disk: {disk}%")

        # 🚨 Alert logic
        if cpu > CPU_THRESHOLD:
            print("⚠️ ALERT: High CPU Usage")

        if mem > MEM_THRESHOLD:
            print("⚠️ ALERT: High Memory Usage")

        if disk > DISK_THRESHOLD:
            print("⚠️ ALERT: High Disk Usage")

    except Exception as e:
        print("❌ Error processing data:", e)

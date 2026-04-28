import socket
import threading
import time

def receive_messages(client):
    while True:
        try:
            data = client.recv(1024)
            if data:
                print(f"Получено: {data.decode('utf-8')}")
        except:
            break

def send_messages(client):
    while True:
        msg = input("Введите сообщение: ")
        if msg:
            client.send(msg.encode('utf-8'))

print("Подключение к серверу...")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5555))
print("Подключено!")

threading.Thread(target=receive_messages, args=(client,), daemon=True).start()
send_messages(client)
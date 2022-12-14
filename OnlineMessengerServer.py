import socket
import threading

s = socket.socket()
port = 30110
s.bind(('', port))
conn_set = set()
s.listen(5)
msg = ""


def message_receiver(clientsocket):
    global msg
    while True:
        print("beginning reception")
        try:
            msg = clientsocket.recv(1024).decode()
        except Exception as e:
            clientsocket.close()
            print("error: client disconnected")
            print(f"[!] Error: {e}")
            conn_set.remove(clientsocket)
            print("list of connections:", conn_set)
            break
        print(msg)


def message_sender():
    global msg
    while True:
        if msg:
            for client in conn_set:
                client.sendall(msg.encode())
            msg = ""


t2 = threading.Thread(target=message_sender)
t2.daemon = True
t2.start()


while True:
    print("accepting connections")
    conn, addr = s.accept()
    print("connection accepted")
    conn_set.add(conn)
    print("list of connections:", conn_set)
    t1 = threading.Thread(target=message_receiver, args=(conn,))
    t1.daemon = True
    t1.start()

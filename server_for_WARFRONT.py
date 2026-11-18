import socket

HOST = "10.44.201.20"
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s :
      s.bind((HOST, PORT))
      s.listen()
      conn, addr = s.accept()
      with conn:
            print(f"connected by {addr}")
            while True:
                  data = conn.recv(1024)
                  if not data:
                        break
                  conn.sendall(data)
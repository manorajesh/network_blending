import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 40674

s.connect(("192.168.32.139", port))

print(s.recv(1024))
s.close()
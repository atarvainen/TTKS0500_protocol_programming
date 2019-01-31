import socket, toiminnallisuus

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("localhost",8888))

data = "A"*2000

toiminnallisuus.send_msg(s, data)

reply = toiminnallisuus.read_msg(s)
print reply
s.close

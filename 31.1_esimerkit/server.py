import socket, toiminnallisuus

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

s.bind(("localhost", 8888))

s.listen(5)

client, addr = s.accept()

msg = toiminnallisuus.read_msg(client)

print msg

toiminnallisuus.send_msg(client, "SAIN T:SERVERI")

client.close()
s.close()

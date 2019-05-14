import paramiko
import sys
from pathlib import Path

# if len(sys.argv)!=2:
#     print("Usage:",sys.argv[0],"user@remoteip")
#     sys.exit(2)

# username,remoteip=sys.argv[1].split('@')
# print(username,remoteip)

# if username==''  or remoteip=='' :
#     print(sys.argv[1],"parse error!")
#     sys.exit(2)
def command_to_car(command_input):
	username = 'pi'
	remoteip = '192.168.32.174'

	homepath=str(Path.home())
	key = paramiko.RSAKey.from_private_key_file(homepath+"/.ssh/id_rsa")
	con = paramiko.SSHClient()

	con.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	print("connecting")
	con.connect(hostname=remoteip, username=username, pkey=key)
	print("connected")

	# commands = ["/bin/ls", "/bin/pwd"]
	
	commands = [command_input]
	# commands = ["ls /home"]
	for command in commands:
		print("Executing {}".format(command))
		stdin,stdout,stderr=con.exec_command(command)
		print(stdout.read().decode('utf-8'))
		print("Errors")
		print(stderr.read().decode('utf-8'))

if __name__ == '__main__':
	pass
# pip install paramiko
# python3 check_ec2_ssh_and_ping.py


import paramiko
import socket

# Configuration
HOST = '13.126.61.48'  # public IP of EC2 instance
USERNAME = 'ubuntu'  # updated username
KEY_PATH = "/mnt/c/Users/mryvs/Downloads/Scrap/GitLab1"  # updated key path (PEM)

def check_ssh_connection(host, username, key_path):
    try:
        key = paramiko.RSAKey.from_private_key_file(key_path)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        print(f"Trying to connect to {host} as {username} ...")
        ssh.connect(hostname=host, username=username, pkey=key, timeout=10)
        
        # Run uname -a to verify connection
        stdin, stdout, stderr = ssh.exec_command('uname -a')
        output = stdout.read().decode()
        print(f"Connection successful! Remote system info:\n{output}")

        # Run ping command to check internet connectivity
        print("Pinging google.com (3 packets)...")
        stdin, stdout, stderr = ssh.exec_command('ping -c 3 google.com')
        ping_output = stdout.read().decode()
        ping_error = stderr.read().decode()
        if ping_output:
            print("Ping output:\n", ping_output)
        if ping_error:
            print("Ping error:\n", ping_error)

        ssh.close()
        return True
    except paramiko.AuthenticationException:
        print("Authentication failed, please check your key or username.")
    except paramiko.SSHException as sshException:
        print(f"Unable to establish SSH connection: {sshException}")
    except socket.timeout:
        print("Connection timed out.")
    except Exception as e:
        print(f"Exception occurred: {e}")
    return False

if __name__ == "__main__":
    check_ssh_connection(HOST, USERNAME, KEY_PATH)


#fabric: A Python library for SSH and remote execution
#by using this script, you can install curl on multiple remote instances in parallel.
#fabric is a powerful tool for automating deployment and system administration tasks.

#below is a sample script to install curl on multiple remote instances using fabric.
#make sure to replace the placeholder values with your actual instance details and SSH key path.
#you need to have fabric installed in your python environment.
#this single script will connect to each instance, update the package list, and install curl.
#you can run this script from your local machine.
#its very useful for managing multiple servers efficiently.

from fabric import Connection, ThreadingGroup
from invoke.exceptions import UnexpectedExit

# Replace with your details
INSTANCES = [
    "13.126.61.48",
    "13.126.61.49",
    "13.126.61.50",
    "13.126.61.51",
    "13.126.61.52",
]

SSH_USER = "ubuntu"
KEY_PATH = "/opt/GitLab.pem" # Path to your SSH private key

def install_curl_on_instance(host):
    try:
        print(f"Connecting to {host}...")
        conn = Connection(
            host=host,
            user=SSH_USER,
            connect_kwargs={"key_filename": KEY_PATH},
            connect_timeout=10,
        )

        # Update package info and install curl (Ubuntu/Debian example)
        print(f"Installing curl on {host}...")
        conn.sudo("apt-get update -y", hide='stdout')
        conn.sudo("apt-get install -y curl", hide='stdout')
        print(f"✅ curl installed on {host}")

    except UnexpectedExit as e:
        print(f"❌ Command failed on {host}: {e.result.stderr.strip()}")
    except Exception as e:
        print(f"❌ Connection or other error on {host}: {e}")

def main():
    # Using ThreadingGroup for parallel execution (Fabric 2.x+)
    group = ThreadingGroup(*INSTANCES, user=SSH_USER, connect_kwargs={"key_filename": KEY_PATH})

    for connection in group:
        try:
            print(f"Connecting to {connection.host}...")
            connection.sudo("apt-get update -y", hide='stdout')
            connection.sudo("apt-get install -y curl", hide='stdout')
            print(f"✅ curl installed on {connection.host}")
        except UnexpectedExit as e:
            print(f"❌ Command failed on {connection.host}: {e.result.stderr.strip()}")
        except Exception as e:
            print(f"❌ Error on {connection.host}: {e}")

if __name__ == "__main__":
    main()

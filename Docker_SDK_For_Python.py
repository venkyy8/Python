#mak e sure to install the docker package first:
#pip install docker

import docker
import time

def run_docker_image(image_name, container_name, port_mapping="8080:80"):
    client = docker.from_env()

    try:
        # Step 1: Pull the image
        print(f"Pulling Docker image: {image_name}")
        client.images.pull(image_name)

        # Step 2: Remove any existing container with the same name
        try:
            existing = client.containers.get(container_name)
            print(f"Removing existing container '{container_name}'...")
            existing.remove(force=True)
        except docker.errors.NotFound:
            pass

        # Step 3: Run the container
        print(f"Running Docker container: {container_name}")
        host_port, container_port = port_mapping.split(":")
        container = client.containers.run(
            image_name,
            name=container_name,
            ports={f'{container_port}/tcp': int(host_port)},
            detach=True
        )

        # Step 4: Wait and check container status
        time.sleep(3)
        container.reload()  # Refresh container status

        if container.status == 'running':
            print(f"✅ Container '{container_name}' is running.")
            print(f"🌐 Access it at http://localhost:{host_port}")
        else:
            print(f"❌ Container '{container_name}' failed to start. Status: {container.status}")
            logs = container.logs().decode()
            print(f"Logs:\n{logs}")

    except docker.errors.DockerException as e:
        print(f"⚠️ Docker SDK error: {e}")
        print("Make sure Docker is installed and running.")

if __name__ == "__main__":
    image_name = "venkyy82/htmlsampleproject:2.0"
    container_name = "html_sample_project_container"
    run_docker_image(image_name, container_name)

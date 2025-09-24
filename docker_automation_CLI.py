import subprocess
import time

def run_docker_image(image_name, container_name, port_mapping="8080:80"):
    try:
        # Step 1: Pull the Docker image
        print(f"Pulling Docker image: {image_name}")
        subprocess.run(["docker", "pull", image_name], check=True)

        # Step 2: Run the Docker container
        print(f"Running Docker container: {container_name}")
        subprocess.run(["docker", "run", "-d", "--name", container_name, "-p", port_mapping, image_name], check=True)

        # Step 3: Wait for a few seconds to ensure the container is up and running
        time.sleep(3)

        # Check if the container is running
        print(f"Checking if the container '{container_name}' is running...")
        container_status = subprocess.run(["docker", "ps", "-q", "-f", f"name={container_name}"], capture_output=True, text=True)

        if container_status.stdout.strip():
            print(f"Container '{container_name}' is running successfully!")
            print(f"Access it on http://localhost:{port_mapping.split(':')[0]}")
        else:
            print(f"Container '{container_name}' is not running. Please check Docker logs.")

    except subprocess.CalledProcessError as e:
        print(f"Error during Docker operation: {e}")
        print("Make sure Docker is installed and running.")
    
if __name__ == "__main__":
    image_name = "venkyy82/htmlsampleproject:2.0"
    container_name = "html_sample_project_container"
    run_docker_image(image_name, container_name)

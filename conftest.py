import pytest
import docker
import time
import requests
import socket


def get_free_port():
    """Find free port on host"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

@pytest.fixture(scope="module")
def container_port():
    """Fixture to get free port for container"""
    return get_free_port()


def wait_for_service(url, timeout=5, interval=0.5):
    """Wait for service to be ready by polling /check endpoint"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"{url}/check")
            if response.status_code == 200:
                return True
        except requests.RequestException:
            pass
        time.sleep(interval)
    raise TimeoutError(f"Service did not become ready within {timeout} seconds")


@pytest.fixture(scope="session")
def docker_client():
    """Fixture to return Docker client"""
    return docker.from_env()

@pytest.fixture(scope="module")
def flask_container(docker_client,container_port,api_base_url):
    """Fixture to provide running service container on desired port for the duration of the tests"""
    # Build image
    image, _ = docker_client.images.build(path=".", tag="hw-test")
    
    # Start container
    container = docker_client.containers.run(
        "hw-test",
        ports={"5000/tcp": container_port},
        detach=True
    )
    
    # Wait for container to be ready
    wait_for_service(api_base_url)
    #time.sleep(2)
    
    yield container
    
    # Stop and remove container
    container.stop()
    container.remove()

@pytest.fixture(scope="module")
def api_base_url(container_port):
    """Fixture to return base URL for API calls"""
    return f"http://localhost:{container_port}"

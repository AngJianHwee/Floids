# Boids Simulation with Pygame and Docker

This project implements a Boids (flocking simulation) using Pygame, packaged within a Docker container. To run the graphical simulation, you will need to enable X11 forwarding.

## Prerequisites

*   Docker installed on your system.
*   An X server running on your host machine.
    *   **macOS:** Install XQuartz (https://www.xquartz.org/). After installation, log out and log back in for changes to take effect.
    *   **Linux:** An X server is usually pre-installed.

## Building the Docker Image

Navigate to the project directory (where `Dockerfile`, `requirements.txt`, and `main.py` are located) and build the Docker image:

```bash
docker build -t boids-simulation .
```

## Running the Docker Container with X11 Forwarding

To display the Pygame window from within the Docker container on your host machine, you need to enable X11 forwarding.

### For Linux Users

1.  Ensure your X server is running.
2.  Grant Docker access to your X server:
    ```bash
    xhost +local:docker
    ```
3.  Run the container with the necessary X11 environment variables and volume mounts:
    ```bash
    docker run -it --rm \
        -e DISPLAY=$DISPLAY \
        -v /tmp/.X11-unix:/tmp/.X11-unix \
        boids-simulation
    ```

### For macOS Users (using XQuartz)

1.  Ensure XQuartz is running.
2.  Open XQuartz preferences (`XQuartz > Preferences...`), go to the "Security" tab, and ensure "Allow connections from network clients" is checked. You might need to restart XQuartz after this change.
3.  Grant Docker access to your X server (replace `your_ip_address` with your host machine's IP address, which you can find using `ifconfig` or `ipconfig`):
    ```bash
    IP_ADDRESS=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')
    xhost + $IP_ADDRESS
    ```
    Alternatively, for simpler local testing (less secure for production):
    ```bash
    xhost +
    ```
4.  Run the container with the necessary X11 environment variables and volume mounts:
    ```bash
    docker run -it --rm \
        -e DISPLAY=host.docker.internal:0 \
        -v /tmp/.X11-unix:/tmp/.X11-unix \
        boids-simulation
    ```
    *Note: `host.docker.internal` is a special DNS name that resolves to the internal IP address of the host from within a Docker container. This is generally preferred over hardcoding your IP address.*

### Explanation of X11 Forwarding Parameters

*   `-e DISPLAY=$DISPLAY`: Passes your host's `DISPLAY` environment variable to the container, telling it where to send graphical output.
*   `-e DISPLAY=host.docker.internal:0`: (macOS specific) Directs the container's graphical output to the X server running on your macOS host via `host.docker.internal`.
*   `-v /tmp/.X11-unix:/tmp/.X11-unix`: Mounts the X11 socket directory from your host into the container, allowing the container to communicate with your X server.
*   `-it`: Runs the container in interactive mode and allocates a pseudo-TTY.
*   `--rm`: Automatically removes the container when it exits.

## Running the Simulation

Once the container is running, the Pygame window should appear on your host machine, displaying the Boids simulation.

import docker

if __name__ == "__main__":
    
    # Create a Docker client
    client = docker.from_env()

    # Run a new container based on the Ubuntu image
    container = client.containers.run('myubuntu', tty=True, stdin_open=True, detach=True)

    # Execute a command inside the container
    output = container.exec_run('pwd')

    # Print the output of the command
    print(output.output.decode('utf-8'))

    # Stop and remove the container
    container.stop()
    container.remove()

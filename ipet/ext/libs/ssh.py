"""Module responsible for ssh connections."""
from paramiko import SSHClient, AutoAddPolicy


def create_ssh_client(server: str, port: int, user: str, password: str) -> SSHClient:
    """Create connection to ssh server.

    Args:
        server (str): Server host.
        port (int): Server port.
        user (str): Server user.
        password (str): Server password.

    Returns:
        SSHClient: returns connected ssh client.
    """
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh.connect(server, port, user, password)
    return ssh

import psutil
import socket
import json


def load_config():
    with open("config/thresholds.json", "r") as file:
        return json.load(file)


def check_cpu():
    return psutil.cpu_percent(interval=1)


def check_memory():
    memory = psutil.virtual_memory()
    return memory.available * 100 / memory.total


def check_disk():
    disk = psutil.disk_usage("/")
    return disk.percent


def check_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(("127.0.0.1", port))
    sock.close()

    if result == 0:
        return False
    return True


def get_server_health():
    config = load_config()

    health = {
        "cpu_usage": check_cpu(),
        "memory_free": check_memory(),
        "disk_usage": check_disk(),
        "port_available": check_port(config["port"])
    }

    return health


if __name__ == "__main__":
    print(get_server_health())
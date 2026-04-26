import sys
import os

# Fix import path issue
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from health_check import get_server_health, load_config


def make_decision():
    health = get_server_health()
    config = load_config()

    reasons = []

    # CPU Check
    if health["cpu_usage"] > config["cpu_limit"]:
        reasons.append("CPU usage is too high")

    # Memory Check
    if health["memory_free"] < config["memory_free_limit"]:
        reasons.append("Memory free is too low")

    # Disk Check
    if health["disk_usage"] > config["disk_limit"]:
        reasons.append("Disk usage is too high")

    # Port Check
    if not health["port_available"]:
        reasons.append("Required port is already in use")

    # Final Decision
    if reasons:
        return {
            "status": "BLOCKED",
            "health": health,
            "reasons": reasons
        }

    return {
        "status": "SUCCESS",
        "health": health,
        "reasons": ["All checks passed"]
    }


if __name__ == "__main__":
    result = make_decision()
    print(result)
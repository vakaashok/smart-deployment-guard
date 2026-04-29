import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from health_check import get_server_health, load_config
from k8s_check import check_kubernetes_pods


def make_decision():
    health = get_server_health()
    config = load_config()
    k8s = check_kubernetes_pods()

    reasons = []

    if health["cpu_usage"] > config["cpu_limit"]:
        reasons.append("CPU usage is too high")

    if health["memory_free"] < config["memory_free_limit"]:
        reasons.append("Memory free is too low")

    if health["disk_usage"] > config["disk_limit"]:
        reasons.append("Disk usage is too high")

    if not health["port_available"]:
        reasons.append("Required port is already in use")

    if k8s["k8s_status"] != "HEALTHY":
        reasons.append("Kubernetes pods are not healthy")

    if reasons:
        return {
            "status": "BLOCKED",
            "health": health,
            "kubernetes": k8s,
            "reasons": reasons
        }

    return {
        "status": "SUCCESS",
        "health": health,
        "kubernetes": k8s,
        "reasons": ["All checks passed"]
    }


if __name__ == "__main__":
    result = make_decision()
    print(result)
import os
import subprocess
from decision_engine import make_decision


def clear_cache():
    print("Self-Healing: Clearing system cache...")
    os.system("sync")
    os.system("echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null")
    print("Cache cleanup attempted")


def show_high_cpu_processes():
    print("Self-Healing: Showing high CPU processes...")
    subprocess.run(["ps", "-eo", "pid,ppid,cmd,%mem,%cpu", "--sort=-%cpu"], check=False)


def restart_service(service_name):
    print(f"Self-Healing: Restarting service: {service_name}")
    subprocess.run(["sudo", "systemctl", "restart", service_name], check=False)


def run_self_healing():
    decision = make_decision()

    if decision["status"] == "SUCCESS":
        print("System healthy. No self-healing needed.")
        return decision

    print("System unhealthy. Self-healing started...")

    for reason in decision["reasons"]:
        if "Memory" in reason:
            clear_cache()

        if "CPU" in reason:
            show_high_cpu_processes()

        if "Disk" in reason:
            print("Disk usage high. Please clean unused files/logs/docker images.")

        if "port" in reason:
            print("Port is busy. Check which process is using the port.")

    print("Self-healing completed. Please re-run deployment.")
    return decision


if __name__ == "__main__":
    run_self_healing()
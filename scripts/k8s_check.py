import subprocess


def check_kubernetes_pods():
    try:
        result = subprocess.run(
            ["kubectl", "get", "pods", "-l", "app=smart-deployment-guard", "--no-headers"],
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode != 0:
            return {
                "k8s_status": "ERROR",
                "message": "Unable to fetch Kubernetes pods",
                "details": result.stderr
            }

        pods_output = result.stdout.strip()

        if not pods_output:
            return {
                "k8s_status": "ERROR",
                "message": "No Kubernetes pods found"
            }

        unhealthy_pods = []

        for line in pods_output.splitlines():
            parts = line.split()
            pod_name = parts[0]
            ready = parts[1]
            status = parts[2]

            if status != "Running" or not ready.startswith("1/1"):
                unhealthy_pods.append({
                    "pod": pod_name,
                    "ready": ready,
                    "status": status
                })

        if unhealthy_pods:
            return {
                "k8s_status": "UNHEALTHY",
                "unhealthy_pods": unhealthy_pods
            }

        return {
            "k8s_status": "HEALTHY",
            "message": "All Kubernetes pods are running"
        }

    except Exception as e:
        return {
            "k8s_status": "ERROR",
            "message": str(e)
        }


if __name__ == "__main__":
    print(check_kubernetes_pods())
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Smart Deployment Guard App Running Successfully!"


@app.route("/health")
def health():
    return {
        "status": "healthy",
        "service": "smart-deployment-guard"
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
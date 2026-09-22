from flask import Flask, jsonify
import os

app = Flask(__name__)


@app.get("/")
def home():
    return jsonify({
        "message": "DevOps application is running!",
        "version": os.getenv("APP_VERSION", "1.0.0"),
    })


@app.get("/health")
def health():
    return jsonify({"status": "healthy"})


@app.get("/version")
def version():
    return jsonify({"version": os.getenv("APP_VERSION", "1.0.0")})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

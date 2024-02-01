from flask import Flask
import psutil
import GPUtil

app = Flask(__name__)

def get_gpu_usage():
    """Returns the GPU usage if NVIDIA GPU is present, else 'Not NVIDIA'."""
    gpus = GPUtil.getGPUs()
    if not gpus:
        return "Not NVIDIA"
    return f"GPU Usage: {gpus[0].load * 100}%"

@app.route('/')
def home():
    """Endpoint to check if the server is up."""
    return "Home"

@app.route('/health')
def health():
    """Endpoint to check if the server is up."""
    return "OK"

@app.route('/usage')
def usage():
    """Endpoint to get current CPU and GPU usage."""
    cpu_usage = psutil.cpu_percent(1)
    gpu_usage = get_gpu_usage()
    return {
        "CPU Usage": f"{cpu_usage}%",
        "GPU Usage": gpu_usage
    }

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=False)


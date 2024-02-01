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
    memory_usage = psutil.virtual_memory()
    disk_usage = psutil.disk_usage('/')
    network_usage = psutil.net_io_counters()
    temp = psutil.sensors_temperatures()
    return {
        "CPU Usage": f"{cpu_usage}%",
        "GPU Usage": gpu_usage,
        "Memory Usage": f"{memory_usage.percent}%",
        "Disk Usage": f"{disk_usage.percent}%",
        "Network Usage": f"{network_usage.bytes_sent} bytes sent, {network_usage.bytes_recv} bytes received",
        "Temperature": f"{temp['coretemp'][0].current}°C"

    }

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=False)


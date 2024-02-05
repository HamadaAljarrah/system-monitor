from flask import Flask
import psutil
import GPUtil
import os
import subprocess
import re

app = Flask(__name__)



# def get_nvidia_gpu_power_usage():
#     """Get the current power usage for NVIDIA GPUs using nvidia-smi."""
#     try:
#         nvidia_smi_output = subprocess.run(['nvidia-smi', '--query-gpu=power.draw', '--format=csv,noheader,nounits'], stdout=subprocess.PIPE, text=True)
#         power_usage_str = nvidia_smi_output.stdout.strip()  # Power usage in watts
#         # In systems with multiple GPUs, this will return the power usage of the first one. Adjust accordingly.
#         power_usage = float(power_usage_str.split('\n')[0])  # Convert first GPU's power usage to float
#         return f"{power_usage} W"
#     except Exception as e:
#         return f"Failed to read GPU power usage: {str(e)}"

def get_nvidia_gpu_power_usage():
    """Get the current power usage for NVIDIA GPUs using nvidia-smi."""
    try:
        nvidia_smi_output = subprocess.run(
            ['nvidia-smi', '--query-gpu=power.draw', '--format=csv,noheader,nounits'],
            stdout=subprocess.PIPE,
            text=True
        )
        power_usage_str = nvidia_smi_output.stdout.strip()  # Power usage in watts
        
        # Handle [N/A] response
        if '[N/A]' in power_usage_str:
            return "Power usage not available for this GPU."
        
        # In systems with multiple GPUs, this will return the power usage of the first one. Adjust accordingly.
        power_usage = float(power_usage_str.split('\n')[0])  # Convert first GPU's power usage to float
        return f"{power_usage} W"
    except Exception as e:
        return f"Failed to read GPU power usage: {str(e)}"




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
    # Example usage
    cpu_energy = psutil.cpu_freq()
    cpu_usage = psutil.cpu_percent(1)
   
    gpu_usage = get_gpu_usage()
    gpu_energy = get_nvidia_gpu_power_usage()
   
    memory_usage = psutil.virtual_memory()
    disk_usage = psutil.disk_usage('/')
    network_usage = psutil.net_io_counters()
    return {
        "CPU Usage": f"{cpu_usage}%",
        "CPU Energy": f"{cpu_energy}",
        "GPU Usage": gpu_usage,
        "Memory Usage": f"{memory_usage.percent}%",
        "Disk Usage": f"{disk_usage.used} bytes used, {disk_usage.free} bytes free, total {disk_usage.total} bytes",
        "Network Usage": f"{network_usage.bytes_sent} bytes sent, {network_usage.bytes_recv} bytes received",
        "GPU Energy": gpu_energy,

    }

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=False)


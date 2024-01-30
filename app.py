import psutil
import time
import GPUtil

def get_gpu_usage():
    """Returns the GPU usage if NVIDIA GPU is present, else 'Not NVIDIA'."""
    gpus = GPUtil.getGPUs()
    if not gpus:
        return "Not NVIDIA"
    return f"GPU Usage: {gpus[0].load * 100}%"

def print_cpu_and_gpu_usage(interval=1):
    """Prints the CPU and GPU usage of the machine every 'interval' seconds."""
    try:
        while True:
            cpu_usage = psutil.cpu_percent(interval)
            gpu_usage = get_gpu_usage()
            print(f"CPU Usage: {cpu_usage}%")
            print(gpu_usage)
    except KeyboardInterrupt:
        print("Program terminated.")

if __name__ == "__main__":
    print_cpu_and_gpu_usage()

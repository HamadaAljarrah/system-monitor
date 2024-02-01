# Use an NVIDIA CUDA image as a parent image, specify the version you need
FROM nvidia/cuda:11.3.1-runtime-ubuntu20.04

# Set the working directory in the container
WORKDIR /usr/src/app

# Install Python and other dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    gcc \
    libc-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN python3.10 -m pip install --upgrade pip

# Copy the current directory contents into the container at /usr/src/app
COPY . /usr/src/app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

# Run app.py when the container launches
CMD ["python3.10", "./app.py"]

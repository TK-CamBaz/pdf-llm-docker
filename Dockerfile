FROM python:3.10-slim

WORKDIR /app

# 1. Install system tools needed to build llama-cpp-python
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libgl1-mesa-glx \
    git \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 2. Install Python packages (gradio, fitz, llama-cpp-python, etc.)
RUN pip install --no-cache-dir \
    gradio \
    PyMuPDF \
    pandas \
    huggingface_hub \
    llama-cpp-python==0.2.38

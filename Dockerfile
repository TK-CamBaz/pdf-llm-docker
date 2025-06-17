FROM python:3.10-slim

WORKDIR /app

# ✅ Install build tools and required libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libgl1-mesa-glx \
    git \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ✅ Install Python dependencies, including llama-cpp-python (will compile)
RUN pip install --no-cache-dir \
    gradio \
    PyMuPDF \
    pandas \
    huggingface_hub \
    llama-cpp-python==0.2.38

# ✅ Copy app code
COPY app.py .

EXPOSE 7860
CMD ["python", "app.py"]

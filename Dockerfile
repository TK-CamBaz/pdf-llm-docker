FROM python:3.10-slim

WORKDIR /app

# System and Python dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx git && \
    pip install --no-cache-dir \
    gradio fitz PyMuPDF pandas llama-cpp-python huggingface_hub

COPY app.py download_models.py models.json ./

# Download model during build (can override ENV later)
ENV MODEL_NAME=phi-2
ENV MODEL_FILE=phi-2.Q4_K_M.gguf
ENV MODEL_PATH=/models/${MODEL_FILE}

RUN python download_models.py

EXPOSE 7860
CMD ["python", "app.py"]


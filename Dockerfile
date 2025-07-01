FROM python:3.10-slim

WORKDIR /app

# Install system and Python dependencies first
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libgl1-mesa-glx \
    git \
    && pip install --no-cache-dir \
    gradio fitz PyMuPDF pandas huggingface_hub llama-cpp-python

# Copy model definitions and download script
COPY models.json download_models.py ./

# Set default model and download it
# This layer will be cached unless the model variables change
ARG MODEL_NAME=phi-2
ARG MODEL_FILE=phi-2.Q4_K_M.gguf
ENV MODEL_NAME=${MODEL_NAME}
ENV MODEL_FILE=${MODEL_FILE}
RUN python download_models.py

# Copy the application code last, so changes to it don't invalidate the model cache
COPY app.py ./

# Expose port and define the command to run the app
EXPOSE 7860
CMD ["python", "app.py"]


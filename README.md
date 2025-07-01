# Local LLM Taxonomic Extractor

This project provides a web-based interface to extract structured taxonomic data from PDF files using a local Large Language Model (LLM). Upload a PDF, specify the traits you want to extract, and the application will return a structured table of the findings.

## Features

- **Simple Web UI:** Built with Gradio for ease of use.
- **PDF Text Extraction:** Uses PyMuPDF to extract text from uploaded PDFs.
- **Local LLM Processing:** Leverages a local LLM (via llama-cpp-python) to analyze text and extract information. This ensures data privacy as no information leaves your machine.
- **Structured Output:** Parses the LLM output into a clean, downloadable CSV file.
- **Containerized:** Ships as a Docker container for easy, cross-platform deployment.

## Deployment and Usage

There are two ways to run this application: using Docker (recommended for portability) or running it locally with Python.

### Option 1: Running with Docker (Recommended)

**Prerequisites:**
- [Docker](https://docs.docker.com/get-docker/) installed on your system.
- A machine with sufficient memory (at least 8GB RAM is recommended) to handle the LLM.

**1. Build the Docker Image:**

Open a terminal in the project root and run:

```bash
docker build -t pdf-extractor .
```

This command builds the image and downloads the default `phi-2` model. This may take some time depending on your internet connection.

**To use a different model (e.g., `tinyllama`):**

You can specify the model at build time. See the `models.json` file for available options.

```bash
docker build --build-arg MODEL_NAME=tinyllama --build-arg MODEL_FILE=tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf -t pdf-extractor .
```

**2. Run the Docker Container:**

Once the build is complete, run the container:

```bash
docker run -p 7860:7860 pdf-extractor
```

**3. Access the Application:**

Open your web browser and navigate to `http://localhost:7860`.

### Option 2: Running Locally with Python

**Prerequisites:**
- Python 3.10 or higher.
- The same system dependencies as in the `Dockerfile`: `build-essential`, `cmake`.

**1. Install Python Dependencies:**

It is highly recommended to use a virtual environment.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**2. Download the LLM Model:**

You need to manually download the model from Hugging Face.

```bash
# Create a directory for the models
mkdir models

# Run the download script
python3 download_models.py
```

This will download the default `phi-2` model into the `models` directory.

**3. Run the Application:**

```bash
python3 app.py
```

**4. Access the Application:**

Open your web browser and navigate to `http://localhost:7860`.

## How to Use the Interface

1.  **Upload PDF:** Click the "Upload PDF" button and select a PDF file from your computer.
2.  **Specify Traits:** In the "Traits to Extract" textbox, enter a comma-separated list of the data you want to find (e.g., `body length, color, habitat`).
3.  **Run:** Click the "Run" button.
4.  **View and Download:** The extracted data will appear in the table. You can then download it as a CSV file using the "Download CSV" button.

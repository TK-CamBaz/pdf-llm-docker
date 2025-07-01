# Rule-Based Species Data Extractor

This script provides a lightweight, fast, and memory-efficient way to extract structured taxonomic data from PDF files. It uses regular expressions (regex) to parse information and does **not** require a Large Language Model (LLM) or a GPU.

This tool is ideal for processing documents with a consistent, well-defined structure.

## Features

- **Gradio Web UI:** An easy-to-use interface to upload PDFs, specify traits, view results, and download a CSV.
- **Flexible Trait Selection:** Specify which traits (sections) to extract via the UI, a command-line argument, or a text file.
- **No LLM Required:** Runs on any machine with Python, no need for large model downloads or high-end hardware.
- **Fast and Efficient:** Processes documents in seconds.
- **Structured JSON/CSV Output:** Extracts key-value data for easy use in other applications.

## Installation and Usage

There are three ways to install and use this tool: using Conda, using Docker, or running it directly with pip.

### Option 1: Using Conda (Recommended for Python Environments)

**Prerequisites:**
- [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) (Miniconda or Anaconda) installed on your system.

**Steps:**

1.  **Navigate to the `regex_extractor` directory:**
    ```bash
    cd /path/to/pdf-llm-docker/regex_extractor
    ```

2.  **Create and activate the Conda environment:**
    ```bash
    conda env create -f conda_env.yaml
    conda activate regex_extractor_env
    ```

3.  **Run the Web UI:**
    ```bash
    python app.py
    ```
    Open your web browser and go to `http://localhost:7860`.

4.  **Run the Command-Line Script:**
    ```bash
    python extractor.py /path/to/your/document.pdf --output extracted_data.json
    ```

### Option 2: Using Docker (Recommended for Containerized Deployment)

**Prerequisites:**
- [Docker](https://docs.docker.com/get-docker/) installed on your system.

**Steps:**

1.  **Navigate to the `regex_extractor` directory:**
    ```bash
    cd /path/to/pdf-llm-docker/regex_extractor
    ```

2.  **Build the Docker image:**
    ```bash
    docker build -t regex-extractor-app .
    ```

3.  **Run the Docker container:**
    ```bash
    docker run -d -p 7860:7860 regex-extractor-app
    ```

4.  **Access the Application:**
    Open your web browser and go to `http://localhost:7860`.

### Option 3: Running Locally with Pip

**Prerequisites:**
- Python 3.6+
- The same system dependencies as in the `Dockerfile` (e.g., `build-essential`, `cmake` on Debian/Ubuntu).

**Steps:**

1.  **Navigate to the `regex_extractor` directory:**
    ```bash
    cd /path/to/pdf-llm-docker/regex_extractor
    ```

2.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Web UI:**
    ```bash
    python app.py
    ```
    Open your web browser and go to `http://localhost:7860`.

4.  **Run the Command-Line Script:**
    ```bash
    python extractor.py /path/to/your/document.pdf --output extracted_data.json
    ```

## How to Use the Interface

1.  **Upload PDF:** Drag and drop or click to upload your PDF file.
2.  **Specify Traits:** A default list of traits is provided. You can edit this list to add, remove, or reorder the sections you want to extract. The order matters.
3.  **Run Extraction:** Click the "Run Extraction" button.
4.  **View and Download:** The extracted data will appear in the table. You can then download it as a CSV file using the "Download CSV" button.

## How to Use the Command-Line Script

The script `extractor.py` is designed for automation. It will now prioritize reading traits from `traits.csv` by default. You can still override this behavior:

-   **Using `traits.csv` (Default):** If you provide no trait arguments, the traits defined in `traits.csv` will be used.
    ```bash
    python extractor.py /path/to/your/document.pdf
    ```

-   **Comma-Separated List:** Use the `--traits` flag to provide a custom list, overriding `traits.csv`.
    ```bash
    python extractor.py /path/to/your/document.pdf --traits "Description,Diagnosis,Distribution"
    ```

-   **Traits File:** Use the `--traits-file` flag to point to a simple text file with one trait per line, overriding `traits.csv`.
    ```bash
    # First, create a file named my_traits.txt:
    # Description
    # Measurements
    # Etymology

    # Then run the script:
    python extractor.py /path/to/your/document.pdf --traits-file my_traits.txt
    ```

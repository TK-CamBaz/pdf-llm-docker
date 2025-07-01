import gradio as gr
import fitz  # PyMuPDF
import pandas as pd
from llama_cpp import Llama
import tempfile
import os
import re

# Get model path from environment variables
MODEL_FILE = os.environ.get("MODEL_FILE", "phi-2.Q4_K_M.gguf")
MODEL_PATH = f"/models/{MODEL_FILE}"

# Load the model once at the beginning
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_threads=4,
    use_mlock=False,
    n_gpu_layers=35
)

def extract_text(pdf_file):
    doc = fitz.open(pdf_file.name)
    return "\n".join(page.get_text() for page in doc)

def run_llm(text, prompt, max_tokens=1024):
    result = llm(prompt=prompt + "\n\n" + text[:4000], max_tokens=max_tokens, stop=["</s>"])
    return result["choices"][0]["text"].strip()

def parse_to_df(llm_output):
    entries = []
    # Use regex to find key-value pairs more robustly
    # This pattern looks for "key: value" and handles variations
    pattern = re.compile(r"'([^']+)'\s*:\s*'([^']*)'")
    
    # Find all matches in the LLM output
    matches = pattern.findall(llm_output)
    
    if matches:
        # Create a DataFrame from the matches
        df = pd.DataFrame(matches, columns=['Attribute', 'Value'])
        # Pivot the table to get the desired format
        df['group'] = (df.index // len(df['Attribute'].unique())).astype(int)
        df = df.pivot(index='group', columns='Attribute', values='Value').reset_index(drop=True)
        return df
    else:
        # Fallback for simple key-value pairs if regex fails
        for block in llm_output.split("\n\n"):
            record = {}
            for line in block.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    record[k.strip()] = v.strip()
            if record:
                entries.append(record)
        return pd.DataFrame(entries)

def process_pdf(pdf_file, traits):
    if not pdf_file:
        return None, None
    text = extract_text(pdf_file)
    prompt = f"Extract the following traits for each species mentioned in the text: {traits}. Also include the species name and the citation."
    llm_output = run_llm(text, prompt)
    df = parse_to_df(llm_output)
    temp_csv = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    df.to_csv(temp_csv.name, index=False)
    return df, temp_csv.name

with gr.Blocks() as demo:
    gr.Markdown("### 🦗 Local LLM Taxonomic Extractor")
    with gr.Row():
        pdf_file = gr.File(label="📄 Upload PDF", file_types=[".pdf"])
        trait_box = gr.Textbox(label="Traits to Extract (comma-separated)", value="body length, color", lines=1)
    run_button = gr.Button("🚀 Run")
    table_output = gr.Dataframe(label="📋 Extracted Table")
    csv_output = gr.File(label="⬇️ Download CSV")

    def handle_run(pdf_file, traits):
        df, csv_path = process_pdf(pdf_file, traits)
        return df, csv_path

    run_button.click(handle_run, inputs=[pdf_file, trait_box], outputs=[table_output, csv_output])

demo.launch(server_name="0.0.0.0", server_port=7860)
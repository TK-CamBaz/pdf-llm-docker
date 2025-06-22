import gradio as gr
import fitz  # PyMuPDF
import pandas as pd
from llama_cpp import Llama
import tempfile
import os

MODEL_PATH = "/models/phi-2.Q4_K_M.gguf"  # Mount this in Docker

def extract_text(pdf_file):
    doc = fitz.open(pdf_file.name)
    return "\n".join(page.get_text() for page in doc)

def run_llm(text, prompt, max_tokens=1024):
    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=2048,
        n_threads=4,
        use_mlock=False,
        n_gpu_layers=35
    )
    result = llm(prompt=prompt + "\n\n" + text[:4000], max_tokens=max_tokens, stop=["</s>"])
    return result["choices"][0]["text"].strip()

def parse_to_df(llm_output):
    entries = []
    for block in llm_output.split("\n\n"):
        record = {}
        for line in block.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                record[k.strip()] = v.strip()
        if record:
            entries.append(record)
    return pd.DataFrame(entries)

def process_pdf(pdf_file, prompt):
    if not pdf_file:
        return None, None
    text = extract_text(pdf_file)
    llm_output = run_llm(text, prompt)
    df = parse_to_df(llm_output)
    temp_csv = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    df.to_csv(temp_csv.name, index=False)
    return df, temp_csv.name

with gr.Blocks() as demo:
    gr.Markdown("### 🦗 Local LLM Taxonomic Extractor")
    with gr.Row():
        pdf_file = gr.File(label="📄 Upload PDF", file_types=[".pdf"])
        prompt_box = gr.Textbox(label="🧠 Prompt", value="Extract all species names, holotype location, traits, and citation.", lines=3)
    run_button = gr.Button("🚀 Run")
    table_output = gr.Dataframe(label="📋 Extracted Table")
    csv_output = gr.File(label="⬇️ Download CSV")

    def handle_run(pdf_file, prompt):
        df, csv_path = process_pdf(pdf_file, prompt)
        return df, csv_path

    run_button.click(handle_run, inputs=[pdf_file, prompt_box], outputs=[table_output, csv_output])

demo.launch()


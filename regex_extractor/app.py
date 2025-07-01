
import gradio as gr
import pandas as pd
import tempfile
import os
from extractor import extract_text_from_pdf, extract_species_data

def process_pdf_for_ui(pdf_file, traits_str):
    if not pdf_file or not traits_str:
        return pd.DataFrame(), None

    # Extract text from the uploaded PDF file object
    text = extract_text_from_pdf(pdf_file.name)
    
    # Get traits from the comma-separated string
    traits = [t.strip() for t in traits_str.split(',') if t.strip()]
    
    # Extract the data
    data = extract_species_data(text, traits)
    
    # Convert the extracted data to a more table-friendly format
    # We will flatten the nested measurement data
    flat_data = []
    if data:
        row = {'species_name': data.get('species_name', 'N/A')}
        for key, value in data.items():
            if key == 'species_name':
                continue
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    row[f'{key}_{sub_key}'] = sub_value
            else:
                row[key] = value
        flat_data.append(row)

    df = pd.DataFrame(flat_data)
    
    # Save to a temporary CSV for download
    if not df.empty:
        temp_csv = tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='w', encoding='utf-8')
        df.to_csv(temp_csv.name, index=False)
        return df, temp_csv.name
    else:
        return df, None

# Define the default list of traits by reading from traits.csv
try:
    with open("traits.csv", 'r') as f:
        DEFAULT_TRAITS = ", ".join([line.strip() for line in f if line.strip()])
except FileNotFoundError:
    DEFAULT_TRAITS = "Description, Coloration, Measurements, Type material, Distribution, Diagnosis, Etymology"

with gr.Blocks() as demo:
    gr.Markdown("### 📄 Rule-Based PDF Taxonomic Extractor")
    gr.Markdown("Upload a PDF and specify the traits (section headers) you want to extract.")

    with gr.Row():
        pdf_file = gr.File(label="📄 Upload PDF", file_types=[".pdf"])
        trait_box = gr.Textbox(
            label="Traits to Extract (comma-separated)", 
            value=DEFAULT_TRAITS, 
            lines=2
        )
    
    run_button = gr.Button("🚀 Run Extraction")
    
    gr.Markdown("### Extracted Data")
    table_output = gr.Dataframe(label="📋 Extracted Table")
    csv_output = gr.File(label="⬇️ Download CSV")

    run_button.click(
        fn=process_pdf_for_ui, 
        inputs=[pdf_file, trait_box], 
        outputs=[table_output, csv_output]
    )

demo.launch(server_name="0.0.0.0", server_port=7860)

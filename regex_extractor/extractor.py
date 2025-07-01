import re
import fitz  # PyMuPDF
import json
import argparse

def extract_text_from_pdf(pdf_path):
    """Extracts all text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def parse_measurements(measurement_text):
    """Parses the measurement string into a structured dictionary."""
    measurements = {}
    # Split by male and female sections
    parts = re.split(r'''(female|male):''', measurement_text, flags=re.IGNORECASE)
    
    current_gender = None
    for part in parts:
        part = part.strip()
        if not part:
            continue
        
        if part.lower() in ['male', 'female']:
            current_gender = part.lower()
            measurements[current_gender] = {}
        elif current_gender:
            # Regex to find trait and its value range (e.g., "body 5.9–6.4")
            matches = re.findall(r'''([a-zA-Z\s]+)\s*([\d.]+[–-][\d.]+)''', part)
            for trait, value in matches:
                measurements[current_gender][trait.strip()] = value.strip()
    return measurements

def extract_species_data(text, traits):
    """Extracts structured data from the species description text using regex."""
    data = {}

    # 1. Species Name (usually at the very beginning)
    species_match = re.search(r'''(.*?sp\. nov\.)''', text)
    if species_match:
        data['species_name'] = species_match.group(1).strip().replace('\n', ' ')

    # 2. Section-based extraction based on the provided traits list
    for i, section in enumerate(traits):
        # Clean the section name for use in regex and dictionary keys
        section_key = section.lower().strip().replace(' ', '_')
        start_pattern = re.compile(f'{section.strip()}\.?(?=\s)', re.IGNORECASE)
        
        # Determine the end pattern (next section or end of text)
        if i + 1 < len(traits):
            end_pattern = re.compile(f'{traits[i+1].strip()}\.?(?=\s)', re.IGNORECASE)
            match = re.search(start_pattern.pattern + '(.*?)' + end_pattern.pattern, text, re.DOTALL)
        else:
            # Last section runs to the end of the text
            match = re.search(start_pattern.pattern + '(.*)', text, re.DOTALL)

        if match:
            content = match.group(1).strip().replace('\n', ' ')
            
            if section.strip().lower() == 'measurements':
                data[section_key] = parse_measurements(content)
            else:
                data[section_key] = content

    return data

def main():
    parser = argparse.ArgumentParser(description="Extract structured data from a species description PDF.")
    parser.add_argument("pdf_path", help="The absolute path to the PDF file.")
    parser.add_argument("--output", default="output.json", help="Path to save the output JSON file.")
    parser.add_argument("--traits", help="A comma-separated list of traits to extract (e.g., 'Description,Coloration').")
    parser.add_argument("--traits-file", help="Path to a text file with one trait per line.")
    args = parser.parse_args()

    # Determine the list of traits to use
    if args.traits:
        traits = [t.strip() for t in args.traits.split(',')]
    elif args.traits_file:
        with open(args.traits_file, 'r') as f:
            traits = [line.strip() for line in f if line.strip()]
    else:
        # Default traits from traits.csv
        try:
            with open("traits.csv", 'r') as f:
                traits = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print("Warning: traits.csv not found. Using hardcoded default traits.")
            traits = ['Description', 'Coloration', 'Measurements', 'Type material', 'Distribution', 'Diagnosis', 'Etymology']

    print(f"Processing {args.pdf_path} using traits: {traits}")
    
    # Extract text from the PDF
    raw_text = extract_text_from_pdf(args.pdf_path)
    
    # Extract structured data using regex
    structured_data = extract_species_data(raw_text, traits)
    
    # Save the output
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(structured_data, f, indent=4, ensure_ascii=False)
        
    print(f"Successfully extracted data to {args.output}")

if __name__ == "__main__":
    main()

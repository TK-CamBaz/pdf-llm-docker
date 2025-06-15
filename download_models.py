import os
import json
from huggingface_hub import snapshot_download

MODEL_NAME = os.environ.get("MODEL_NAME", "phi-2")
MODEL_FILE = os.environ.get("MODEL_FILE", "phi-2.Q4_K_M.gguf")
DEST = "/models"

with open("models.json") as f:
    MODELS = json.load(f)

if MODEL_NAME not in MODELS:
    raise ValueError(f"Unknown model: {MODEL_NAME}. Options: {list(MODELS.keys())}")

print(f"🔽 Downloading {MODEL_NAME} model...")
snapshot_download(repo_id=MODELS[MODEL_NAME], local_dir=DEST, local_dir_use_symlinks=False)
print("✅ Download completed.")


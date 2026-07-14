import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

#product ka base foldr path 
BASE_DIR = Path(__file__).resolve().parent.parent

#---- LLM settings ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")



LLM_MODEL = "llama-3.3-70b-versatile"
LLM_TEMPERATURE = 0.1

#----Folder Path---
DATA_DIR = BASE_DIR / "data"
SAMPLE_ASSETS_DIR = DATA_DIR / "sample_assets"
OUTPUTS_DIR = BASE_DIR / "outputs"
ASSET_CONTEXT_FILE=DATA_DIR/"asset_context.json"
ACTIVATION_HISOTRY_FILE=DATA_DIR/"activation_history.csv"


TAXONOMY_FILE = DATA_DIR / "taxonomy_schema.json"
BRAND_GUIDELINES_FILE = DATA_DIR / "brand_guidelines.txt"
PRODUCT_INFO_FILE = DATA_DIR / "product_info.json"
HISTORICAL_PERFORMANCE_FILE = DATA_DIR / "historical_performance.csv"


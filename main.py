from src.extract_data import extract_weather_data
from src.transform_data import data_transformations
from src.load_data import load_weather_data

import os
from pathlib import Path
from dotenv import load_dotenv

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
load_dotenv(env_path)

API_KEY =  os.getenv('api_key')

url = f"https://api.openweathermap.org/data/2.5/weather?q=Sao%20Paulo&units=metric&appid={API_KEY}"
table_name = 'sp_weather'

def pipeline():
    
    try:
        logging.info("ETAPA 1: extract...")
        extract_weather_data(url)

        logging.info("ETAPA 2: transform...")
        df = data_transformations()

        logging.info("ETAPA 3: load...")
        load_weather_data(table_name, df)

        print("\nPipeline concluído!")

    except:
        logging.error(f"Erro no pipeline: {e}")
        import traceback
        traceback.print_exc()

pipeline()
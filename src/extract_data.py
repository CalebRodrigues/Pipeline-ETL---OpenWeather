import requests
import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_weather_data(url:str) -> list:

    # Faz a requisição pelo url e armazena na variável
    response = requests.get(url)

    # Variável recebe a resposta da requissição e transforma em dicionário
    data = response.json()

    if response.status_code != 200:
        logging.error("Erro na requisição")
        return []

    if not data:
        logging.warning("Nenhum dado retornado")
        return []

    # Caminho que será exportado o arquivo json
    output_path = 'data/weather_data.json'

    # Extrai apenas o diretório do caminho para garantir que a pasta de destino exista
    output_dir = Path(output_path).parent

    # Cria o diretório (parents=True cria as pastas intermediárias se não existirem; exist_ok=True evita erros caso a pasta já exista)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Abre o arquivo no caminho indicado em modo de escrita ('w') e o apelida de 'f'
    with open(output_path, 'w') as f:

        # Converte o objeto Python (data) em formato JSON e escreve-o dentro do arquivo aberto (f)
        json.dump(data, f, indent=4)

    logging.info(f"Arquivo salvo em {output_path}!")

    return data
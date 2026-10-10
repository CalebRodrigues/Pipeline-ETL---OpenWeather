import pandas as pd
from pathlib import Path
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

path_name = Path(__file__).parent.parent / 'data' / 'weather_data.json'

colums_names_to_drop = ['weather', 'weather_icon', 'sys.type']

colums_names_to_rename = {
    'cod': 'code',
    'coord.lon': 'longitude',
    'coord.lat': 'latitude',
    'main.temp': 'temperature',
    'main.feels_like': 'feels_like',
    'main.temp_min': 'temp_min',
    'main.temp_max': 'temp_max',
    'main.pressure': 'pressure',
    'main.humidity': 'humidity',
    'main.sea_level': 'sea_level',
    'main.grnd_level': 'grnd_level',
    'wind.speed': 'wind_speed',
    'wind.deg': 'wind_deg',
    'wind.gust': 'wind_gust',
    'clouds.all': 'clouds',
    'sys.type': 'sys_type',
    'sys.id': 'sys_id',
    'sys.country': 'country',
    'sys.sunrise': 'sunrise',
    'sys.sunset': 'sunset'
}

columns_names_to_normalize = ['sunset', 'sunrise', 'dt']

def create_dataframe(path_name: str) -> pd.DataFrame:

    path = path_name

    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    with open(path) as f:
        data = json.load(f)

    df = pd.json_normalize(data)

    logging.info(f"\n DataFrame criado com {len(df)} linha(s)")

    return df

def normalize_weather_columns(df: pd.DataFrame) -> pd.DataFrame:

    df_weather = pd.json_normalize(df['weather'].apply(lambda x: x[0]))

    df_weather = df_weather.rename(columns = {
        'id': 'weather_id',
        'main': 'weather_main',
        'description': 'weather_description',
        'icon': 'weather_icon'
    })

    df = pd.concat([df, df_weather], axis=1)

    logging.info(f"\n Coluna 'weather' normalizada - {len(df.columns)} colunas")

    return df

def drop_columns(df: pd.DataFrame, columns_names: list[str]) -> pd.DataFrame:

    logging.info(f"Removendo colunas: {columns_names}")

    df =df.drop(columns=columns_names)

    logging.info(f"Colunas removidas - {len(df.columns)} colunas restantes")

    return df

def rename_columns(df: pd.DataFrame, colums_names_to_rename:dict[str, str]) -> pd.DataFrame:

    logging.info(f"Renomeando {len(colums_names_to_rename)} coluna(s)")

    df = df.rename(columns=colums_names_to_rename)

    logging.info(f"Colunas renomeadas!")

    return df

def normalize_datetime_columns(df: pd.DataFrame, columns_names: list[str]) -> pd.DataFrame:
    """
    Normaliza colunas contendo timestamps Unix para o formato de data/hora oficial,
    convertendo-as para o fuso horário de São Paulo.
    """
    logging.info("\nNormalizando datetime...")

    # Percorre cada nome de coluna passado na lista 'columns_names'
    for name in columns_names:

        # Converte o valor numérico (segundos Unix) num objeto datetime em UTC e em seguida ajusta para o fuso horário local de São Paulo ('America/Sao_Paulo'
        df[name] = pd.to_datetime(df[name], unit='s', utc=True).dt.tz_convert('America/Sao_Paulo')

    logging.info("Normalizado com sucesso!\n")

    # Retorna o DataFrame modificado
    return df

def data_transformations():

    print("\nIniciando transformações...")

    df = create_dataframe(path_name)
    df = normalize_weather_columns(df)
    df = drop_columns(df, colums_names_to_drop)
    df = rename_columns(df, colums_names_to_rename)
    df = normalize_datetime_columns(df, columns_names_to_normalize)

    print("\nTransformações concluídas")

    return df
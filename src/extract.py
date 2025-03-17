import requests
import pandas as pd
import sys
from typing import Dict

def get_brazil_holidays(year: int) -> pd.DataFrame:
    """Obtiene los días festivos de Brasil para un año específico."""
    url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/BR"
    try:
        response = requests.get(url)
        response.raise_for_status()
        holidays = response.json()
        df = pd.DataFrame(holidays)
        df = df.drop(columns=['counties', 'types'], errors='ignore')  # Elimina columnas innecesarias
        df['date'] = pd.to_datetime(df['date'])
        df = df.rename(columns={'date': 'datetime'})  # Renombra columna para consistencia
        return df
    except requests.exceptions.RequestException as e:
        print(f"----- ERROR al obtener los días festivos de {year}: {e} -----")
        sys.exit(1)

def extract(csv_folder: str, csv_table_mapping: Dict[str, str], years: list) -> Dict[str, pd.DataFrame]:
    """Extrae datos de archivos CSV y festivos de Brasil."""
    # Lectura de archivos CSV en DataFrames
    dataframes = {
        table_name: pd.read_csv(f"{csv_folder}/{csv_file}")
        for csv_file, table_name in csv_table_mapping.items()
    }
    
    # Obtención de días festivos por año
    holidays_by_year = {}
    for year in years:
        holidays_df = get_brazil_holidays(year)
        if holidays_df is not None:
            holidays_by_year[f"public_holidays_{year}"] = holidays_df
    
    # Combina ambos diccionarios y devuelve los resultados
    dataframes.update(holidays_by_year)
    return dataframes

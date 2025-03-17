import os
import pandas as pd
import sqlite3
from typing import Dict

def load(dataframes: Dict[str, pd.DataFrame], db_name: str) -> None:
    """Carga los DataFrames en una base de datos SQLite."""
    try:
        # Asegúrate de que la carpeta exista antes de intentar guardar el archivo de base de datos
        db_folder = os.path.dirname(db_name)
        if not os.path.exists(db_folder):
            os.makedirs(db_folder)
            print(f"Carpeta creada: {db_folder}")
        
        # Conexión a la base de datos SQLite
        conn = sqlite3.connect(db_name)
        for table_name, dataframe in dataframes.items():
            # Guarda cada DataFrame como tabla en la base de datos
            dataframe.to_sql(name=table_name, con=conn, if_exists='replace', index=False)
            print(f"Tabla '{table_name}' cargada exitosamente.")
        
        # Cierra la conexión a la base de datos
        conn.close()
        print("Conexión a la base de datos cerrada.")
    except Exception as e:
        print(f"Error al cargar los DataFrames en la base de datos: {e}")

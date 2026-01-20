import pandas as pd
import os

from src.cargar_fichero import CargarFichero

class ExportarDatos:
    def __init__(self, datos: CargarFichero):
        self.datos = datos
    
    def exportar(self):
        self.datos.df.to_parquet("data/finanzas.parquet", engine="pyarrow", compression="snappy")
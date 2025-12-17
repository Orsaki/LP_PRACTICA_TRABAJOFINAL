import requests
import pandas as pd

# --- CONFIGURACIÓN ---
# 1. Lista de países de Sudamérica
paises_sudamerica = [
    'ARG', 'BOL', 'BRA', 'CHL', 'COL', 'ECU', 
    'GUY', 'PRY', 'PER', 'SUR', 'URY', 'VEN'
]
codigos_paises = ';'.join(paises_sudamerica)

# 2. Indicadores ACTUALIZADOS
indicadores = {
    'NY.GDP.MKTP.CD': 'PBI_USD',           # PBI (Dólares)
    'SP.POP.TOTL':    'Poblacion',         # Población Total
    'SI.POV.NAHC':    'Pobreza_Nacional',  # Tasa de Pobreza (% Nacional)
    'FP.CPI.TOTL.ZG': 'Inflacion_Anual',   # Inflación (% anual precios consumidor)
    'SI.POV.GINI':    'Indice_Gini'        # Desigualdad (0-100)
}

# --- FUNCIÓN DE EXTRACCIÓN (Igual que antes) ---
def obtener_datos_wb(indicador, codigos_paises):
    # Pedimos datos desde 2019 para asegurar encontrar datos de Gini (que no siempre es anual)
    url = f"http://api.worldbank.org/v2/country/{codigos_paises}/indicator/{indicador}?format=json&date=2019:2024&per_page=1000"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if len(data) < 2:
            return []
            
        resultados = []
        for item in data[1]:
            if item['value'] is not None:
                resultados.append({
                    'Codigo_ISO': item['countryiso3code'],
                    'País': item['country']['value'],
                    'Año': item['date'],
                    'Valor': item['value'],
                    'Indicador': indicador # Guardamos esto para referencia
                })
        return resultados
    except Exception as e:
        print(f"Error descargando {indicador}: {e}")
        return []

# --- EJECUCIÓN ---
print("Conectando a la API del Banco Mundial...")
todos_los_datos = []

for codigo_ind, nombre_columna in indicadores.items():
    print(f"Descargando datos de: {nombre_columna} ({codigo_ind})...")
    datos = obtener_datos_wb(codigo_ind, codigos_paises)
    
    df_temp = pd.DataFrame(datos)
    
    if not df_temp.empty:
        # LÓGICA IMPORTANTE: Ordenar por Año descendente y quedarse con el primero (el más reciente)
        df_temp = df_temp.sort_values('Año', ascending=False).drop_duplicates('Codigo_ISO')
        
        # Renombrar columna Valor
        df_temp = df_temp[['Codigo_ISO', 'País', 'Valor']].rename(columns={'Valor': nombre_columna})
        
        todos_los_datos.append(df_temp)

# --- UNIÓN FINAL ---
if todos_los_datos:
    df_final = todos_los_datos[0]
    for df in todos_los_datos[1:]:
        df_final = pd.merge(df_final, df, on=['Codigo_ISO', 'País'], how='outer')

    # Ajustes de formato para leer mejor
    if 'PBI_USD' in df_final.columns:
        df_final['PBI_Billions'] = df_final['PBI_USD'] / 1e9 # Miles de millones
        
    if 'Poblacion' in df_final.columns:
        df_final['Poblacion_Millones'] = df_final['Poblacion'] / 1e6 # Millones

    # Seleccionamos y ordenamos las columnas para verlas mejor
    columnas_ordenadas = [
        'País', 'Codigo_ISO', 'Año', # Año del dato base (puedes ajustar esto si prefieres)
        'PBI_Billions', 'Poblacion_Millones', 
        'Pobreza_Nacional', 'Inflacion_Anual', 'Indice_Gini'
    ]
    
    # Filtramos solo las columnas que existen (por si alguna falló)
    cols_a_mostrar = [c for c in columnas_ordenadas if c in df_final.columns]
    
    print("\n--- TABLA FINAL DE DATOS SUDAMÉRICA ---")
    print(df_final[cols_a_mostrar])
    
    # Opcional: Guardar en Excel o CSV
    # df_final.to_csv('datos_sudamerica.csv', index=False)
    # print("Guardado en 'datos_sudamerica.csv'")

else:
    print("No se pudieron obtener datos.")
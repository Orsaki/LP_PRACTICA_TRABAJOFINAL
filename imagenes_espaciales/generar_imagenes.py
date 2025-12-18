import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- CONFIGURACIÓN ---
paises_sudamerica = ['ARG','BOL','BRA','CHL','COL','ECU','GUY','PRY','PER','SUR','URY','VEN']
codigos_paises = ';'.join(paises_sudamerica)

indicadores = {
    'NY.GDP.MKTP.CD': 'PBI_USD',
    'SP.POP.TOTL': 'Poblacion',
    'SI.POV.NAHC': 'Pobreza_Nacional',
    'FP.CPI.TOTL.ZG': 'Inflacion_Anual',
    'SI.POV.GINI': 'Indice_Gini'
}

# --- FUNCION DE DESCARGA ---
def obtener_datos_wb(indicador, codigos_paises):
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
                    'Indicador': indicador
                })
        return resultados
    except Exception as e:
        print(f"Error descargando {indicador}: {e}")
        return []

# --- DESCARGA DE DATOS ---
todos_los_datos = []

for cod, nombre in indicadores.items():
    datos = obtener_datos_wb(cod, codigos_paises)
    df_temp = pd.DataFrame(datos)
    if not df_temp.empty:
        df_temp = df_temp.sort_values('Año', ascending=False).drop_duplicates('Codigo_ISO')
        df_temp = df_temp[['Codigo_ISO','País','Valor']].rename(columns={'Valor': nombre})
        todos_los_datos.append(df_temp)

if todos_los_datos:
    df_final = todos_los_datos[0]
    for df in todos_los_datos[1:]:
        df_final = pd.merge(df_final, df, on=['Codigo_ISO','País'], how='outer')

    # Ajustes de formato
    if 'PBI_USD' in df_final.columns:
        df_final['PBI_Billions'] = df_final['PBI_USD']/1e9
    if 'Poblacion' in df_final.columns:
        df_final['Poblacion_Millones'] = df_final['Poblacion']/1e6
else:
    print("No se pudieron obtener datos.")
    exit()

# --- CREAR CARPETA DE IMÁGENES ---
carpeta_imagenes = "imagenes_espaciales"
if not os.path.exists(carpeta_imagenes):
    os.makedirs(carpeta_imagenes)

# --- CONFIGURACIÓN VISUAL ---
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10,6)

# --- 1. Inflación ---
if 'Inflacion_Anual' in df_final.columns:
    df_inf = df_final[['País','Inflacion_Anual']].sort_values('Inflacion_Anual', ascending=False).set_index('País')
    plt.figure(figsize=(6,8))
    sns.heatmap(df_inf, annot=True, cmap='Reds', fmt=".1f", cbar_kws={'label':'Inflación Anual (%)'})
    plt.title('Inflación Anual Sudamérica')
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_imagenes,'inflacion_sudamerica.png'))
    plt.close()

# --- 2. Desigualdad (Gini) ---
if 'Indice_Gini' in df_final.columns:
    df_gini = df_final.sort_values('Indice_Gini', ascending=False).set_index('País')
    plt.figure(figsize=(10,6))
    sns.barplot(x=df_gini['Indice_Gini'], y=df_gini.index, palette='viridis')
    plt.title('Desigualdad Social Sudamérica (Índice Gini)')
    plt.xlabel('Gini')
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_imagenes,'desigualdad_gini.png'))
    plt.close()

# --- 3. PBI per cápita ---
if 'PBI_Billions' in df_final.columns and 'Poblacion_Millones' in df_final.columns:
    df_final['PBI_Per_Capita'] = (df_final['PBI_Billions']/df_final['Poblacion_Millones'])*1000
    df_pc = df_final.sort_values('PBI_Per_Capita', ascending=False).set_index('País')
    plt.figure(figsize=(10,6))
    sns.barplot(x=df_pc['PBI_Per_Capita'], y=df_pc.index, palette='Blues_d')
    plt.title('PBI per Cápita Sudamérica (USD)')
    plt.xlabel('USD por Habitante')
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_imagenes,'pbi_per_capita.png'))
    plt.close()

print("¡Imágenes generadas y guardadas en la carpeta 'imagenes_espaciales'!")

import requests
import pandas as pd
import numpy as np

url = "https://data360api.worldbank.org/data360/data"

# indicador del PBI en el perú
parametros = {
    "DATABASE_ID": "WB_WDI",
    "REF_AREA": "PER",
    "INDICATOR": "WB_WDI_NY_GDP_MKTP_KD"  
}

response = requests.get(url, params=parametros)
json_data = response.json()
df = pd.DataFrame(json_data['value'])
cols = ['TIME_PERIOD', 'OBS_VALUE']
df_limpio = df[cols].copy()

#print(df_limpio.info())
# convertimos los datos a otro tipo de dato para analizarla
# veremos antes si existe valores nulos

print(df_limpio.isnull().sum())

# no hay valores nulos en caso halla usar drop.na()

df_limpio['TIME_PERIOD'] = df_limpio['TIME_PERIOD'].astype(int)
df_limpio['OBS_VALUE'] = pd.to_numeric(df_limpio['OBS_VALUE'], errors= 'coerce') # si tiene nulos colocará NaN

#print(df_limpio.info())

#print(df_limpio.head(10))
print(df_limpio.iloc[-1]) #ultimo año registrado fue 2024 

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
plt.scatter(df_limpio['TIME_PERIOD'], df_limpio['OBS_VALUE'], 
             color='#2E86C1', 
             linewidth=2.5,
             label='PIB Perú')

plt.title('Evolución del PIB de Perú', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Año', fontsize=12)
plt.ylabel('PIB', fontsize=12)
plt.xticks(rotation=45)
plt.show()

# dado que vemos puntos con curvatura o en forma de S y dado que solo tenemos dos variables, una opción es aplicar regresion polinomica

y = df_limpio['OBS_VALUE']
x = df_limpio['TIME_PERIOD']
z = np.polyfit(x,y,3) #se calculo coeficientes 
p = np.poly1d(z) #creamos funcion 

#predicciones 

prediccion = p(2025)
print(f"La prediccion en 2025 del PBI del perú en soles es de : {prediccion/1e9:.2f} miles de millones de soles")

#261598136780.0  = 2.61 x 10^11
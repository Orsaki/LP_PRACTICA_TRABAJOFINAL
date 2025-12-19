import requests
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf

from statsmodels.formula.api import ols


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

y = df_limpio['OBS_VALUE']
x = df_limpio['TIME_PERIOD']

# Análisis descriptivo 

sns.scatterplot(x,y,data=df_limpio)


# grafico lineal
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))
sns.regplot(x='TIME_PERIOD', y='OBS_VALUE', data=df_limpio,
                    ax=ax1,
                    order=1,
                    line_kws={'color': 'red'},
                    scatter_kws={'alpha': 0.5})
ax1.set_title('Modelo Lineal', fontsize=14)
ax1.set_ylabel('PIB')

#linea de regresion de grado 3
sns.regplot(x='TIME_PERIOD', y='OBS_VALUE', data=df_limpio,
                    ax=ax2,
                    order=3,
                    line_kws={'color': 'green'},
                    scatter_kws={'alpha': 0.5})

ax2.set_title('Modelo Polinómico G3 (R² ≈ 0.98)', fontsize=14)
plt.show()


# Es mejor hacerlo con el paquete OLS
formula = "OBS_VALUE ~ TIME_PERIOD + I(TIME_PERIOD**2) + I(TIME_PERIOD**3)"
modelo_poli = ols(formula, df_limpio).fit()
print(modelo_poli.summary())
mod_lineal = ols("OBS_VALUE ~ TIME_PERIOD", data=df_limpio).fit()
print(mod_lineal.summary())

# Vemos muchas medidas estadistica, pruebas, IC.
# # Ahora estamos interesados en saber que modelo explica mejor al PBI
# Para ello usaremos una medida de bondad de ajuste como el R2

# modelo lineal

r2_lineal = mod_lineal.rsquared
r2_poly = modelo_poli.rsquared
if r2_poly > r2_lineal:
    print(f"El modelo polinomial explica mejor al PBI con un r2 de {round(r2_poly,2)*100} %")
else:
    print(f"El modelo lineal explica mejor al PBI con un r2 de {round(r2_lineal,2)*100} %")
# hemos decidido que el mejor modelo por el coportamiento de datos es ek de ro_poly es yaor

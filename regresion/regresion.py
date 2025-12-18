import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import os
from statsmodels.stats.stattools import durbin_watson
from statsmodels.graphics.gofplots import qqplot

# --- 1. CARGA DE DATOS ---
ruta_archivo = os.path.join("archivos csv", "datos_sudamerica.csv")
df = pd.read_csv(ruta_archivo)

# Creamos la carpeta donde guardaremos resultados y gráficos
carpeta_resultados = "regresion"
os.makedirs(carpeta_resultados, exist_ok=True)

# --- 2. PREPARACIÓN DE VARIABLES ---
df = df.copy()
# Calculamos PBI per cápita
df['PBI_Per_Capita'] = (df['PBI_Billions'] / df['Poblacion_Millones']) * 1000

# Eliminamos filas con NaN en las variables de interés
df_reg = df[['Pobreza_Nacional','Inflacion_Anual','Indice_Gini','PBI_Per_Capita']].dropna()

X = df_reg[['Inflacion_Anual','Indice_Gini','PBI_Per_Capita']]
y = df_reg['Pobreza_Nacional']
X = sm.add_constant(X)  # Agregar constante para el intercepto

# --- 3. AJUSTE DE MODELO DE REGRESIÓN ---
modelo = sm.OLS(y, X).fit()

# Guardamos resultados en CSV
df_resultados = modelo.summary2().tables[1]
df_resultados.to_csv(os.path.join(carpeta_resultados, "regresion_pobreza.csv"))

# --- 4. GRÁFICOS DE DIAGNÓSTICO ---
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (8,6)

# a) QQ Plot (normalidad)
plt.figure()
qqplot(modelo.resid, line='s')
plt.title("QQ Plot de los residuos")
plt.tight_layout()
plt.savefig(os.path.join(carpeta_resultados, "qq_residuos.png"))
plt.close()

# b) Residuos vs Ajustados (homocedasticidad)
plt.figure()
plt.scatter(modelo.fittedvalues, modelo.resid, color='blue', edgecolor='black')
plt.axhline(y=0, color='red', linestyle='--')
plt.xlabel("Valores ajustados")
plt.ylabel("Residuos")
plt.title("Residuos vs Valores Ajustados")
plt.tight_layout()
plt.savefig(os.path.join(carpeta_resultados, "residuos_vs_ajustados.png"))
plt.close()

# c) Histograma de residuos
plt.figure()
sns.histplot(modelo.resid, kde=True, color='purple')
plt.title("Distribución de los residuos")
plt.xlabel("Residuos")
plt.ylabel("Frecuencia")
plt.tight_layout()
plt.savefig(os.path.join(carpeta_resultados, "hist_residuos.png"))
plt.close()

# d) Durbin-Watson (autocorrelación)
dw = durbin_watson(modelo.resid)
with open(os.path.join(carpeta_resultados, "durbin_watson.txt"), "w") as f:
    f.write(f"Durbin-Watson statistic: {dw:.3f}\n")

print("Regresión realizada, CSV y gráficos guardados en la carpeta 'regresion'.")

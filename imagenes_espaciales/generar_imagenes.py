# generar_imagenes_nuevas.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- 1. CARGA DE DATOS ---
ruta_archivo = os.path.join("archivos csv", "datos_sudamerica.csv")
df = pd.read_csv(ruta_archivo)
df = df.set_index('País')

# Carpeta para guardar imágenes
carpeta_imagenes = "imagenes_espaciales"
os.makedirs(carpeta_imagenes, exist_ok=True)

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10,6)

# --- 2. SCATTER PBI vs Pobreza ---
if 'PBI_Billions' in df.columns and 'Pobreza_Nacional' in df.columns:
    df['PBI_Per_Capita'] = (df['PBI_Billions'] / df['Poblacion_Millones'])*1000
    plt.figure(figsize=(10,6))
    sns.scatterplot(data=df, x='PBI_Per_Capita', y='Pobreza_Nacional', s=150, color='green', edgecolor='black')
    for pais in df.index:
        plt.text(df.loc[pais,'PBI_Per_Capita']*1.01, df.loc[pais,'Pobreza_Nacional'], pais, fontsize=9)
    plt.title('Relación PBI per Cápita vs. Pobreza Nacional')
    plt.xlabel('PBI per Cápita (USD)')
    plt.ylabel('Tasa de Pobreza (%)')
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_imagenes,'pbi_vs_pobreza.png'))
    plt.close()

# --- 3. SCATTER Inflación vs Gini ---
if 'Inflacion_Anual' in df.columns and 'Indice_Gini' in df.columns:
    plt.figure(figsize=(10,6))
    sns.scatterplot(data=df, x='Inflacion_Anual', y='Indice_Gini', s=150, color='purple', edgecolor='black')
    for pais in df.index:
        plt.text(df.loc[pais,'Inflacion_Anual']*1.01, df.loc[pais,'Indice_Gini'], pais, fontsize=9)
    plt.title('Relación Inflación vs. Índice Gini')
    plt.xlabel('Inflación Anual (%)')
    plt.ylabel('Gini')
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_imagenes,'inflacion_vs_gini.png'))
    plt.close()

# --- 4. HISTOGRAMA DE POBLACIÓN ---
if 'Poblacion_Millones' in df.columns:
    plt.figure(figsize=(10,6))
    sns.histplot(df['Poblacion_Millones'], bins=8, kde=True, color='orange')
    plt.title('Distribución de la Población (Millones)')
    plt.xlabel('Millones de Habitantes')
    plt.ylabel('Cantidad de Países')
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_imagenes,'poblacion_histograma.png'))
    plt.close()

# --- 5. MAPA DE CALOR DE CORRELACIONES ---
columnas_indicadores = ['Inflacion_Anual','Indice_Gini','PBI_Per_Capita','Pobreza_Nacional']
df_corr = df[columnas_indicadores].corr()
plt.figure(figsize=(8,6))
sns.heatmap(df_corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Mapa de Calor: Correlaciones entre Indicadores')
plt.tight_layout()
plt.savefig(os.path.join(carpeta_imagenes,'correlaciones_indicadores.png'))
plt.close()

print("✅ Imágenes nuevas generadas en la carpeta 'imagenes_espaciales'.")

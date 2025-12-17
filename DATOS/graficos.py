import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- 1. CARGA DE DATOS ---
ruta_archivo = os.path.join("archivos csv", "datos_sudamerica.csv")
print(f"Leyendo datos desde: {ruta_archivo}...")

try:
    df = pd.read_csv(ruta_archivo)
    df = df.set_index('País') # Usamos el país como índice para las etiquetas
    print("¡Datos cargados correctamente!")
except FileNotFoundError:
    print("Error: No se encuentra el archivo 'datos_sudamerica.csv'. Ejecuta primero el script de descarga.")
    exit()

# --- 2. CONFIGURACIÓN VISUAL GENERAL ---
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# ==============================================================================
# GRÁFICO 1: EL TERMÓMETRO DE INFLACIÓN (Heatmap)
# ==============================================================================
# Muestra rápidamente qué países tienen la economía "más caliente" (inestable).
if 'Inflacion_Anual' in df.columns:
    # Ordenamos de mayor a menor
    df_inflacion = df[['Inflacion_Anual']].sort_values(by='Inflacion_Anual', ascending=False)
    
    plt.figure(figsize=(6, 8)) # Formato vertical
    
    sns.heatmap(df_inflacion, 
                annot=True,           # Poner los números dentro de los cuadros
                cmap='Reds',          # Color Rojo: Más intenso = Más peligro
                fmt=".1f",            # 1 decimal
                cbar_kws={'label': 'Inflación Anual (%)'},
                linewidths=1,         # Borde blanco entre celdas
                linecolor='white')
    
    plt.title('Ranking: Inflación Anual (%)', fontsize=16)
    plt.tight_layout()
    plt.show()


# ==============================================================================
# GRÁFICO 2: RANKING DE DESIGUALDAD (GINI)
# ==============================================================================
# Compara qué tan equitativa es la distribución de riqueza.
if 'Indice_Gini' in df.columns:
    # Ordenamos de mayor a menor desigualdad
    df_gini = df.sort_values('Indice_Gini', ascending=False)

    plt.figure(figsize=(12, 6))
    
    grafico = sns.barplot(x=df_gini['Indice_Gini'], y=df_gini.index, palette='viridis')
    
    plt.title('Desigualdad Social en Sudamérica (Índice Gini)', fontsize=16)
    plt.xlabel('Índice Gini (0 = Igualdad Perfecta, 100 = Desigualdad Total)')
    
    # Agregamos los valores al final de las barras
    plt.bar_label(grafico.containers[0], fmt='%.1f', padding=3)
    
    plt.tight_layout()
    plt.show()


# ==============================================================================
# GRÁFICO 3: RELACIÓN INFLACIÓN VS. POBREZA (Scatter Plot)
# ==============================================================================
# Analiza si el aumento de precios golpea a la pobreza.
if 'Inflacion_Anual' in df.columns and 'Pobreza_Nacional' in df.columns:
    plt.figure(figsize=(12, 8))
    
    # Scatter plot: Eje X = Inflación, Eje Y = Pobreza
    sns.scatterplot(data=df, x='Inflacion_Anual', y='Pobreza_Nacional', 
                    s=200,                # Tamaño de los puntos
                    color='darkorange',   # Color de los puntos
                    alpha=0.8,            # Transparencia
                    edgecolor='black')    # Borde negro en los puntos

    # Etiquetar cada punto con el nombre del país
    for pais in df.index:
        x_pos = df.loc[pais, 'Inflacion_Anual']
        y_pos = df.loc[pais, 'Pobreza_Nacional']
        
        # Ajustamos el texto un poco a la derecha (+0.5) para que no tape el punto
        plt.text(x_pos + 0.5, y_pos, pais, fontsize=10, fontweight='bold')

    # Líneas de referencia (Promedios)
    plt.axvline(x=df['Inflacion_Anual'].mean(), color='red', linestyle='--', alpha=0.5, label='Promedio Inflación')
    plt.axhline(y=df['Pobreza_Nacional'].mean(), color='blue', linestyle='--', alpha=0.5, label='Promedio Pobreza')
    plt.legend()

    plt.title('Análisis: Impacto de la Inflación en la Pobreza', fontsize=16)
    plt.xlabel('Inflación Anual (%)', fontsize=12)
    plt.ylabel('Tasa de Pobreza Nacional (%)', fontsize=12)
    
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()


# ==============================================================================
# GRÁFICO 4: RIQUEZA REAL POR HABITANTE (PBI PER CÁPITA)
# ==============================================================================
# Este gráfico revela el verdadero nivel de vida, eliminando el efecto "país grande".

if 'PBI_Billions' in df.columns and 'Poblacion_Millones' in df.columns:
    # 1. Calculamos el PBI Per Cápita (Miles de Millones / Millones = Miles de USD)
    # Multiplicamos por 1000 para tener el dato exacto en Dólares
    df['PBI_Per_Capita'] = (df['PBI_Billions'] / df['Poblacion_Millones']) * 1000
    
    # 2. Ordenamos para el ranking
    df_per_capita = df.sort_values('PBI_Per_Capita', ascending=False)

    plt.figure(figsize=(12, 6))
    
    # Usamos un gráfico de barras horizontales
    grafico = sns.barplot(x=df_per_capita['PBI_Per_Capita'], y=df_per_capita.index, palette='Blues_d')
    
    plt.title('Ranking de Riqueza Promedio: PBI Per Cápita (USD)', fontsize=16)
    plt.xlabel('Dólares por Habitante (USD anual)', fontsize=12)
    
    # Agregamos el signo de dólar a las etiquetas
    # Usamos un bucle simple para formatear bonito "$ 15,300"
    for i, container in enumerate(grafico.containers):
        grafico.bar_label(container, fmt='$ %.0f', padding=3)

    plt.grid(axis='x', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()
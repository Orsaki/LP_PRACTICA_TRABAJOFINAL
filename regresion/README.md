# Análisis de Regresión: Pobreza Nacional en Sudamérica

Esta carpeta contiene el análisis de regresión realizado sobre el dataset de Sudamérica, enfocándose en la variable dependiente **Pobreza_Nacional** y sus posibles predictores: **Inflacion_Anual**, **Indice_Gini** y **PBI_Per_Capita**.

## Contenido de la carpeta

| Archivo | Descripción |
|---------|-------------|
| `regresion.py` | Script en Python que realiza la regresión lineal y genera los gráficos de diagnóstico. |
| `regresion_pobreza.csv` | Resultados de la regresión (coeficientes, errores estándar, t-stat, p-values). |
| `hist_residuos.png` | Histograma de los residuos del modelo para evaluar normalidad. |
| `qq_residuos.png` | Gráfico Q-Q de los residuos para verificar distribución normal. |
| `residuos_vs_ajustados.png` | Gráfico de residuos vs valores ajustados para evaluar homocedasticidad. |
| `durbin_watson.txt` | Resultado de la prueba de Durbin-Watson para detectar autocorrelación. |
| `README.md` | Este archivo, que describe la carpeta y su contenido. |

## Cómo ejecutar

1. Asegúrate de tener instaladas las librerías necesarias: `pandas`, `matplotlib`, `seaborn`, `statsmodels`.
2. Ejecuta el script `regresion.py` para recrear los gráficos de diagnóstico y generar los resultados en CSV.
3. Revisa los archivos generados para interpretar la regresión y validar supuestos.

## Observaciones

- La muestra utilizada es pequeña (12 países) por lo que los resultados deben interpretarse con cautela.
- Se verificaron supuestos de normalidad y homocedasticidad mediante gráficos y pruebas estadísticas.
- El análisis permite identificar la relación de los indicadores económicos con la pobreza nacional y visualizar patrones generales en Sudamérica.



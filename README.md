# 📊 Dashboard de Métricas 2025

Dashboard interactivo para análisis de ventas, stock, devoluciones y métricas de negocio 2025.

## 🚀 Deploy en Streamlit Cloud

Este dashboard está listo para desplegarse en [Streamlit Community Cloud](https://share.streamlit.io).

### Pasos para desplegar:

1. **Sube este repositorio a GitHub**
   ```bash
   cd dashboard-metricas-2025
   git init
   git add .
   git commit -m "Initial commit: Dashboard Métricas 2025"
   git branch -M main
   git remote add origin https://github.com/tu-usuario/dashboard-metricas-2025.git
   git push -u origin main
   ```

2. **Despliega en Streamlit Cloud**
   - Ve a [share.streamlit.io](https://share.streamlit.io)
   - Haz clic en "New app"
   - Selecciona tu repositorio
   - Branch: `main`
   - Main file path: `app.py`
   - Haz clic en "Deploy"

3. **¡Listo!** Tu dashboard estará disponible en una URL como:
   `https://tu-usuario-dashboard-metricas-2025-app-xxxxx.streamlit.app`

## 🏃‍♂️ Ejecutar localmente

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar dashboard
streamlit run app.py
```

El dashboard se abrirá en `http://localhost:8501`

## 📁 Estructura del proyecto

```
dashboard-metricas-2025/
├── app.py                          # Aplicación principal de Streamlit
├── analisis_2025_completo.csv     # Datos de análisis
├── requirements.txt                # Dependencias Python
├── .streamlit/
│   └── config.toml                # Configuración de Streamlit
├── .gitignore                     # Archivos ignorados por Git
└── README.md                      # Este archivo
```

## 📊 Características

- **5 pestañas de análisis**:
  - 📊 Evolución Temporal
  - 🎯 Por Vertical (Libro, Música, Película, Videojuego)
  - 👥 Por Autor
  - 🗂️ Por Categoría
  - 📦 Devoluciones
  - 📋 Tabla Detallada

- **Filtros interactivos**:
  - Meses, verticales, idiomas, formatos, categorías, autores
  - Filtros de valores mínimos/máximos
  - Selector de columnas personalizable

- **KPIs principales**:
  - Total ventas, cancelaciones, devoluciones
  - Ratios de devolución y rotación
  - Stock activo

- **Visualizaciones**:
  - Gráficos de líneas, barras, heatmaps
  - Análisis de costes de envío
  - Top productos y autores
  - Tabla exportable a CSV

## 🛠️ Tecnologías

- **Streamlit** 1.31.0 - Framework de dashboard
- **Pandas** 2.1.4 - Análisis de datos
- **Plotly** 5.18.0 - Visualizaciones interactivas

## 📝 Notas

- El CSV incluido contiene ~5.3M de filas con todas las combinaciones de métricas
- Los datos están pre-agregados por mes, vertical, idioma, formato, categoría y autor
- El dashboard reagrupa dinámicamente según las columnas seleccionadas

## 📄 Licencia

MIT

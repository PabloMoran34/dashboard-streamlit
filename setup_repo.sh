#!/bin/bash

# Script para inicializar el repositorio Git y subir a GitHub

echo "📦 Inicializando repositorio Git..."
git init

echo "📝 Añadiendo archivos..."
git add .

echo "💾 Creando commit inicial..."
git commit -m "Initial commit: Dashboard Métricas 2025

- Dashboard interactivo con Streamlit
- Análisis de ventas, stock, devoluciones 2025
- Filtros avanzados y visualizaciones con Plotly
- Listo para deploy en Streamlit Cloud"

echo "🌿 Cambiando a branch main..."
git branch -M main

echo ""
echo "✅ Repositorio inicializado!"
echo ""
echo "📌 Próximos pasos:"
echo "1. Crea un repositorio en GitHub (https://github.com/new)"
echo "2. Ejecuta estos comandos (reemplaza TU-USUARIO y TU-REPO):"
echo ""
echo "   git remote add origin https://github.com/TU-USUARIO/TU-REPO.git"
echo "   git push -u origin main"
echo ""
echo "3. Ve a https://share.streamlit.io y despliega tu app"
echo ""

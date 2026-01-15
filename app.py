#!/usr/bin/env python3
"""
Dashboard interactivo para análisis de métricas 2025
Usar: streamlit run dashboard_metricas.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Configuración de la página
st.set_page_config(
    page_title="Análisis Métricas 2025",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados
st.markdown("""
    <style>
    .main {
        padding: 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 5px;
    }
    .stMetric label {
        color: #262730 !important;
        font-weight: 600;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #0e1117 !important;
        font-size: 1.5rem;
    }
    .stMetric [data-testid="stMetricDelta"] {
        color: #262730 !important;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Carga los datos sin dimensión de autor (optimizado)"""
    parquet_path = "analisis_2025_sin_autor.parquet"
    if not os.path.exists(parquet_path):
        st.error(f"❌ No se encontró el archivo: {parquet_path}")
        st.info("Dataset no encontrado")
        st.stop()
    
    df = pd.read_parquet(parquet_path)
    return df


def main():
    # Título principal
    st.title("📊 Dashboard de Métricas 2025")
    st.markdown("---")
    
    # Cargar datos
    df = load_data()
    
    # ==========================
    # SIDEBAR - FILTROS
    # ==========================
    st.sidebar.header("🔍 Filtros")
    
    # Inicializar session_state para los filtros si no existe
    if 'reset_filters' not in st.session_state:
        st.session_state.reset_filters = False
    
    # Obtener valores únicos de cada campo
    all_months = sorted([x for x in df['mes'].unique() if pd.notna(x)])
    all_verticals = sorted([x for x in df['vertical'].unique() if pd.notna(x)])
    all_languages = sorted([x for x in df['idioma'].unique() if pd.notna(x)])
    all_formats = sorted([x for x in df['formato'].unique() if pd.notna(x)])
    all_categories = sorted([x for x in df['categoria'].unique() if pd.notna(x)])
    
    # Botón de reseteo de filtros
    if st.sidebar.button("🔄 Resetear Filtros", use_container_width=True):
        st.session_state.reset_filters = True
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Determinar valores por defecto (todos si reset o valores previos)
    if st.session_state.reset_filters:
        default_months = all_months
        default_verticals = all_verticals
        default_languages = all_languages
        default_formats = all_formats
        default_categories = all_categories
        st.session_state.reset_filters = False
    else:
        default_months = st.session_state.get('selected_months', all_months)
        default_verticals = st.session_state.get('selected_verticals', all_verticals)
        default_languages = st.session_state.get('selected_languages', all_languages)
        default_formats = st.session_state.get('selected_formats', all_formats)
        default_categories = st.session_state.get('selected_categories', all_categories)
    
    # Filtro de meses
    selected_months = st.sidebar.multiselect(
        "Meses",
        options=all_months,
        default=default_months,
        key='selected_months'
    )
    
    # Filtro de verticales
    selected_verticals = st.sidebar.multiselect(
        "Verticales",
        options=all_verticals,
        default=default_verticals,
        key='selected_verticals'
    )
    
    # Filtro de idiomas
    selected_languages = st.sidebar.multiselect(
        "Idiomas",
        options=all_languages,
        default=default_languages,
        key='selected_languages'
    )
    
    # Filtro de formatos
    selected_formats = st.sidebar.multiselect(
        "Formatos",
        options=all_formats,
        default=default_formats,
        key='selected_formats'
    )
    
    # Filtro de categorías
    selected_categories = st.sidebar.multiselect(
        "Categorías",
        options=all_categories,
        default=default_categories,
        key='selected_categories'
    )
    
    # Nota sobre optimización
    st.sidebar.info("ℹ️ Dataset optimizado sin dimensión de autor (141K filas, 0.8MB)")
    
    # Aplicar filtros
    df_filtered = df[
        (df['mes'].isin(selected_months)) &
        (df['vertical'].isin(selected_verticals)) &
        (df['idioma'].isin(selected_languages)) &
        (df['formato'].isin(selected_formats)) &
        (df['categoria'].isin(selected_categories))
    ]
    
    st.sidebar.markdown("---")
    st.sidebar.metric("Filas totales", len(df))
    st.sidebar.metric("Filas filtradas", len(df_filtered))
    
    # ==========================
    # KPIs PRINCIPALES
    # ==========================
    st.header("📈 KPIs Principales")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_ventas = df_filtered['ventas'].sum()
        st.metric("Total Ventas", f"{total_ventas:,.0f}")
    
    with col2:
        total_cancelaciones = df_filtered['cancelaciones'].sum()
        st.metric("Total Cancelaciones", f"{total_cancelaciones:,.0f}")
    
    with col3:
        total_devoluciones = df_filtered['devoluciones'].sum()
        st.metric("Total Devoluciones", f"{total_devoluciones:,.0f}")
    
    with col4:
        ratio_devolucion_avg = df_filtered['ratio_devoluciones'].mean()
        st.metric("Ratio Devolución", f"{ratio_devolucion_avg:.2%}")
    
    with col5:
        rotacion_avg = df_filtered[df_filtered['rotacion'] > 0]['rotacion'].mean()
        st.metric("Rotación Promedio", f"{rotacion_avg:.3f}")
    
    st.markdown("---")
    
    # ==========================
    # TABS DE VISUALIZACIONES
    # ==========================
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Evolución Temporal",
        "🎯 Por Vertical",
        "🗂️ Por Categoría",
        "📦 Devoluciones",
        "📋 Tabla Detallada"
    ])
    
    # ===== TAB 1: EVOLUCIÓN TEMPORAL =====
    with tab1:
        st.subheader("Evolución de Ventas por Mes")
        
        # Ventas por mes y vertical
        ventas_mes = df_filtered.groupby(['mes', 'vertical'])['ventas'].sum().reset_index()
        
        fig = px.line(
            ventas_mes,
            x='mes',
            y='ventas',
            color='vertical',
            markers=True,
            title="Ventas por Mes y Vertical"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Dos gráficos en columnas
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Precio Medio Venta vs Compra")
            precios_mes = df_filtered.groupby('mes').agg({
                'precio_medio_venta': 'mean',
                'precio_medio_compra': 'mean'
            }).reset_index()
            
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=precios_mes['mes'],
                y=precios_mes['precio_medio_venta'],
                name='Precio Venta',
                mode='lines+markers',
                line=dict(color='green')
            ))
            fig2.add_trace(go.Scatter(
                x=precios_mes['mes'],
                y=precios_mes['precio_medio_compra'],
                name='Precio Compra',
                mode='lines+markers',
                line=dict(color='#2E8B57')
            ))
            fig2.update_layout(height=350, xaxis_title="Mes", yaxis_title="Precio (€)")
            st.plotly_chart(fig2, use_container_width=True)
        
        with col2:
            st.subheader("Stock Activo por Mes")
            stock_mes = df_filtered.groupby(['mes', 'vertical'])['stock_activo'].sum().reset_index()
            
            fig3 = px.bar(
                stock_mes,
                x='mes',
                y='stock_activo',
                color='vertical',
                title="Stock Activo Mensual"
            )
            fig3.update_layout(height=350)
            st.plotly_chart(fig3, use_container_width=True)
        
        # Heatmap mes x vertical
        st.subheader("Heatmap: Ventas por Mes y Vertical")
        pivot_ventas = df_filtered.pivot_table(
            values='ventas',
            index='vertical',
            columns='mes',
            aggfunc='sum',
            fill_value=0
        )
        
        fig4 = px.imshow(
            pivot_ventas,
            labels=dict(x="Mes", y="Vertical", color="Ventas"),
            color_continuous_scale='Blues',
            aspect="auto"
        )
        fig4.update_layout(height=300)
        st.plotly_chart(fig4, use_container_width=True)
    
    # ===== TAB 2: POR VERTICAL =====
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Ventas por Vertical")
            ventas_vertical = df_filtered.groupby('vertical')['ventas'].sum().reset_index()
            ventas_vertical = ventas_vertical.sort_values('ventas', ascending=False)
            
            fig5 = px.bar(
                ventas_vertical,
                x='vertical',
                y='ventas',
                color='vertical',
                title="Total Ventas por Vertical"
            )
            fig5.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig5, use_container_width=True)
        
        with col2:
            st.subheader("Ratio Cancelación por Vertical")
            cancel_vertical = df_filtered.groupby('vertical').agg({
                'ventas': 'sum',
                'cancelaciones': 'sum'
            }).reset_index()
            cancel_vertical['ratio'] = cancel_vertical['cancelaciones'] / (
                cancel_vertical['ventas'] + cancel_vertical['cancelaciones']
            )
            
            fig6 = px.bar(
                cancel_vertical,
                x='vertical',
                y='ratio',
                color='vertical',
                title="Ratio de Cancelación por Vertical"
            )
            fig6.update_layout(showlegend=False, height=400, yaxis_tickformat='.1%')
            st.plotly_chart(fig6, use_container_width=True)
        
        st.subheader("Rotación por Vertical")
        rotacion_vertical = df_filtered[df_filtered['rotacion'] > 0].groupby('vertical')['rotacion'].mean().reset_index()
        rotacion_vertical = rotacion_vertical.sort_values('rotacion', ascending=True)
        
        fig7 = px.bar(
            rotacion_vertical,
            x='rotacion',
            y='vertical',
            orientation='h',
            color='vertical',
            title="Rotación Promedio por Vertical"
        )
        fig7.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig7, use_container_width=True)
    
    # ===== TAB 3: POR CATEGORÍA =====
    with tab3:
        st.subheader("Top 15 Categorías por Ventas")
        
        categorias_ventas = df_filtered.groupby('categoria').agg({
            'ventas': 'sum',
            'stock_activo': 'sum',
            'rotacion': 'mean'
        }).reset_index()
        categorias_ventas = categorias_ventas[categorias_ventas['categoria'] != 'Desconocido']
        categorias_ventas = categorias_ventas.sort_values('ventas', ascending=False).head(15)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig9 = px.bar(
                categorias_ventas,
                x='ventas',
                y='categoria',
                orientation='h',
                title="Ventas por Categoría"
            )
            fig9.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig9, use_container_width=True)
        
        with col2:
            fig10 = px.bar(
                categorias_ventas,
                x='rotacion',
                y='categoria',
                orientation='h',
                title="Rotación por Categoría",
                color='rotacion',
                color_continuous_scale='Viridis'
            )
            fig10.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig10, use_container_width=True)
    
    # ===== TAB 4: DEVOLUCIONES =====
    with tab4:
        st.subheader("Análisis de Devoluciones")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Devoluciones por Vertical")
            dev_vertical = df_filtered.groupby('vertical').agg({
                'devoluciones': 'sum',
                'ventas': 'sum'
            }).reset_index()
            dev_vertical['ratio_dev'] = dev_vertical['devoluciones'] / (
                dev_vertical['ventas'] + dev_vertical['devoluciones']
            )
            
            fig_dev1 = px.bar(
                dev_vertical,
                x='vertical',
                y='devoluciones',
                color='vertical',
                title="Total Devoluciones por Vertical"
            )
            fig_dev1.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig_dev1, use_container_width=True)
        
        with col2:
            st.subheader("Ratio Devolución por Vertical")
            fig_dev2 = px.bar(
                dev_vertical,
                x='vertical',
                y='ratio_dev',
                color='vertical',
                title="Ratio de Devolución por Vertical"
            )
            fig_dev2.update_layout(showlegend=False, height=400, yaxis_tickformat='.1%')
            st.plotly_chart(fig_dev2, use_container_width=True)
        
        # Evolución temporal de devoluciones
        st.subheader("Evolución de Devoluciones por Mes")
        dev_mes = df_filtered.groupby(['mes', 'vertical'])['devoluciones'].sum().reset_index()
        
        fig_dev3 = px.line(
            dev_mes,
            x='mes',
            y='devoluciones',
            color='vertical',
            markers=True,
            title="Devoluciones Mensuales"
        )
        fig_dev3.update_layout(height=400)
        st.plotly_chart(fig_dev3, use_container_width=True)
        
        # Costes de envío
        st.subheader("Análisis de Costes de Envío")
        
        col1, col2 = st.columns(2)
        
        with col1:
            coste_mes = df_filtered.groupby('mes')['coste_medio_envio'].mean().reset_index()
            fig_coste1 = px.line(
                coste_mes,
                x='mes',
                y='coste_medio_envio',
                markers=True,
                title="Coste Medio de Envío por Mes"
            )
            fig_coste1.update_layout(height=350, yaxis_title="Coste (€)")
            st.plotly_chart(fig_coste1, use_container_width=True)
        
        with col2:
            coste_vertical = df_filtered.groupby('vertical')['coste_medio_envio'].mean().reset_index()
            fig_coste2 = px.bar(
                coste_vertical,
                x='vertical',
                y='coste_medio_envio',
                color='vertical',
                title="Coste Medio de Envío por Vertical"
            )
            fig_coste2.update_layout(showlegend=False, height=350, yaxis_title="Coste (€)")
            st.plotly_chart(fig_coste2, use_container_width=True)
        
        # Top categorías con más devoluciones
        st.subheader("Top 15 Categorías con Más Devoluciones")
        dev_cat = df_filtered.groupby('categoria').agg({
            'devoluciones': 'sum',
            'ventas': 'sum'
        }).reset_index()
        dev_cat = dev_cat[dev_cat['categoria'] != 'Desconocido']
        dev_cat['ratio_dev'] = dev_cat['devoluciones'] / (dev_cat['ventas'] + dev_cat['devoluciones'])
        dev_cat = dev_cat.sort_values('devoluciones', ascending=False).head(15)
        
        fig_dev4 = px.bar(
            dev_cat,
            x='devoluciones',
            y='categoria',
            orientation='h',
            color='ratio_dev',
            color_continuous_scale='Reds',
            title="Categorías con más devoluciones (color = ratio)"
        )
        fig_dev4.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_dev4, use_container_width=True)
    
    # ===== TAB 5: TABLA DETALLADA =====
    with tab5:
        st.subheader("Datos Detallados")
        
        # Selector de columnas
        all_columns = df_filtered.columns.tolist()
        default_columns = ['mes', 'vertical', 'idioma', 'formato', 'categoria', 
                          'ventas', 'stock_activo', 'rotacion', 'precio_medio_venta']
        
        selected_columns = st.multiselect(
            "📋 Seleccionar columnas a mostrar",
            options=all_columns,
            default=[col for col in default_columns if col in all_columns],
            help="Elige las columnas que quieres visualizar en la tabla"
        )
        
        if not selected_columns:
            st.warning("⚠️ Selecciona al menos una columna para mostrar")
            st.stop()
        
        # Filtros de valores mínimos
        st.markdown("#### 🔢 Filtros de Valores Mínimos")
        filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
        
        with filter_col1:
            min_ventas = st.number_input(
                "Ventas mínimas", 
                min_value=0, 
                max_value=1000, 
                value=0, 
                step=1,
                help="Filtrar filas con al menos N ventas"
            )
        
        with filter_col2:
            min_stock = st.number_input(
                "Stock mínimo", 
                min_value=0, 
                max_value=1000, 
                value=0, 
                step=1,
                help="Filtrar filas con al menos N unidades de stock"
            )
        
        with filter_col3:
            min_rotacion = st.number_input(
                "Rotación mínima", 
                min_value=0.0, 
                max_value=10.0, 
                value=0.0, 
                step=0.1,
                format="%.1f",
                help="Filtrar filas con rotación >= N"
            )
        
        with filter_col4:
            min_precio = st.number_input(
                "Precio venta mínimo (€)", 
                min_value=0.0, 
                max_value=100.0, 
                value=0.0, 
                step=1.0,
                format="%.2f",
                help="Filtrar filas con precio medio >= N"
            )
        
        # Segunda fila de filtros adicionales (opcional, en expander)
        with st.expander("➕ Filtros adicionales"):
            filter_col5, filter_col6, filter_col7, filter_col8 = st.columns(4)
            
            with filter_col5:
                min_devoluciones = st.number_input(
                    "Devoluciones mínimas", 
                    min_value=0, 
                    max_value=100, 
                    value=0, 
                    step=1,
                    help="Filtrar filas con al menos N devoluciones"
                )
            
            with filter_col6:
                min_cancelaciones = st.number_input(
                    "Cancelaciones mínimas", 
                    min_value=0, 
                    max_value=100, 
                    value=0, 
                    step=1,
                    help="Filtrar filas con al menos N cancelaciones"
                )
            
            with filter_col7:
                max_ratio_dev = st.number_input(
                    "Ratio devolución máximo", 
                    min_value=0.0, 
                    max_value=1.0, 
                    value=1.0, 
                    step=0.05,
                    format="%.2f",
                    help="Filtrar filas con ratio devolución <= N"
                )
            
            with filter_col8:
                max_ratio_cancel = st.number_input(
                    "Ratio cancelación máximo", 
                    min_value=0.0, 
                    max_value=1.0, 
                    value=1.0, 
                    step=0.05,
                    format="%.2f",
                    help="Filtrar filas con ratio cancelación <= N"
                )
        
        # Opciones de visualización
        st.markdown("#### ⚙️ Opciones de Visualización")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Todos los campos numéricos disponibles
            sort_by = st.selectbox(
                "Ordenar por",
                ['ventas', 'devoluciones', 'cancelaciones', 'stock_activo', 'rotacion', 
                 'precio_medio_venta', 'precio_medio_compra', 'ratio_cancelaciones',
                 'ratio_devoluciones', 'coste_medio_envio']
            )
        
        with col2:
            sort_order = st.radio("Orden", ['Descendente', 'Ascendente'])
        
        with col3:
            n_rows = st.number_input(
                "Número de filas", 
                min_value=10, 
                max_value=10000, 
                value=100, 
                step=50
            )
        
        # Aplicar filtros de valores mínimos
        df_to_display = df_filtered.copy()
        
        filters_applied = []
        if min_ventas > 0:
            df_to_display = df_to_display[df_to_display['ventas'] >= min_ventas]
            filters_applied.append(f"ventas >= {min_ventas}")
        
        if min_stock > 0:
            df_to_display = df_to_display[df_to_display['stock_activo'] >= min_stock]
            filters_applied.append(f"stock >= {min_stock}")
        
        if min_rotacion > 0:
            df_to_display = df_to_display[df_to_display['rotacion'] >= min_rotacion]
            filters_applied.append(f"rotación >= {min_rotacion:.1f}")
        
        if min_precio > 0:
            df_to_display = df_to_display[df_to_display['precio_medio_venta'] >= min_precio]
            filters_applied.append(f"precio >= €{min_precio:.2f}")
        
        if min_devoluciones > 0:
            df_to_display = df_to_display[df_to_display['devoluciones'] >= min_devoluciones]
            filters_applied.append(f"devoluciones >= {min_devoluciones}")
        
        if min_cancelaciones > 0:
            df_to_display = df_to_display[df_to_display['cancelaciones'] >= min_cancelaciones]
            filters_applied.append(f"cancelaciones >= {min_cancelaciones}")
        
        if max_ratio_dev < 1.0:
            df_to_display = df_to_display[df_to_display['ratio_devoluciones'] <= max_ratio_dev]
            filters_applied.append(f"ratio dev <= {max_ratio_dev:.0%}")
        
        if max_ratio_cancel < 1.0:
            df_to_display = df_to_display[df_to_display['ratio_cancelaciones'] <= max_ratio_cancel]
            filters_applied.append(f"ratio cancel <= {max_ratio_cancel:.0%}")
        
        # Identificar columnas categóricas y numéricas en la selección
        categorical_cols = ['mes', 'vertical', 'idioma', 'formato', 'categoria']
        selected_categorical = [col for col in selected_columns if col in categorical_cols]
        selected_numeric = [col for col in selected_columns if col not in categorical_cols]
        
        # Si hay columnas categóricas seleccionadas, reagrupar
        if selected_categorical:
            # Definir cómo agregar cada columna numérica
            agg_dict = {}
            
            if 'stock_activo' in selected_numeric:
                agg_dict['stock_activo'] = 'sum'
            if 'ventas' in selected_numeric:
                agg_dict['ventas'] = 'sum'
            if 'cancelaciones' in selected_numeric:
                agg_dict['cancelaciones'] = 'sum'
            if 'devoluciones' in selected_numeric:
                agg_dict['devoluciones'] = 'sum'
            if 'rotacion' in selected_numeric:
                agg_dict['rotacion'] = 'mean'
            if 'precio_medio_venta' in selected_numeric:
                agg_dict['precio_medio_venta'] = 'mean'
            if 'precio_medio_compra' in selected_numeric:
                agg_dict['precio_medio_compra'] = 'mean'
            if 'ratio_cancelaciones' in selected_numeric:
                agg_dict['ratio_cancelaciones'] = 'mean'
            if 'ratio_devoluciones' in selected_numeric:
                agg_dict['ratio_devoluciones'] = 'mean'
            if 'coste_medio_envio' in selected_numeric:
                agg_dict['coste_medio_envio'] = 'mean'
            
            # Reagrupar
            if agg_dict:
                df_to_display = df_to_display.groupby(selected_categorical, as_index=False).agg(agg_dict)
            else:
                # Solo columnas categóricas, obtener combinaciones únicas
                df_to_display = df_to_display[selected_categorical].drop_duplicates()
        else:
            # Solo columnas numéricas seleccionadas, sumar todo
            if selected_numeric:
                totals = df_to_display[selected_numeric].sum().to_frame().T
                df_to_display = totals
            else:
                st.warning("⚠️ Selecciona al menos una columna")
                st.stop()
        
        # Mostrar contador y filtros aplicados
        if filters_applied:
            filters_text = " | ".join(filters_applied)
            st.caption(f"Mostrando {min(n_rows, len(df_to_display)):,} de {len(df_to_display):,} filas agrupadas (filtros: {filters_text})")
        else:
            st.caption(f"Mostrando {min(n_rows, len(df_to_display)):,} de {len(df_to_display):,} filas agrupadas (sin filtros mínimos)")
        
        # Ordenar solo si la columna de ordenación está seleccionada
        if sort_by in df_to_display.columns:
            df_display = df_to_display.sort_values(
                sort_by,
                ascending=(sort_order == 'Ascendente')
            ).head(n_rows)
        else:
            df_display = df_to_display.head(n_rows)
            st.info(f"ℹ️ La columna '{sort_by}' no está seleccionada. Mostrando primeras {n_rows} filas sin ordenar por ella.")
        
        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True,
            height=500
        )
        
        # Botón de descarga
        csv = df_display.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="⬇️ Descargar datos filtrados (CSV)",
            data=csv,
            file_name="metricas_filtradas.csv",
            mime="text/csv"
        )
        
        # Estadísticas de la tabla (solo mostrar si las columnas están seleccionadas)
        st.markdown("### Estadísticas de datos agrupados")
        
        # Crear métricas dinámicamente basadas en columnas seleccionadas
        stats_to_show = []
        if 'ventas' in df_display.columns:
            stats_to_show.append(("Total Ventas", f"{df_display['ventas'].sum():,.0f}"))
        if 'devoluciones' in df_display.columns:
            stats_to_show.append(("Total Devoluciones", f"{df_display['devoluciones'].sum():,.0f}"))
        if 'stock_activo' in df_display.columns:
            stats_to_show.append(("Total Stock Activo", f"{df_display['stock_activo'].sum():,.0f}"))
        if 'rotacion' in df_display.columns:
            stats_to_show.append(("Rotación Media", f"{df_display['rotacion'].mean():.3f}"))
        if 'precio_medio_venta' in df_display.columns:
            stats_to_show.append(("Precio Venta Medio", f"€{df_display['precio_medio_venta'].mean():.2f}"))
        
        if stats_to_show:
            cols = st.columns(len(stats_to_show))
            for i, (label, value) in enumerate(stats_to_show):
                with cols[i]:
                    st.metric(label, value)
        else:
            st.info("💡 Selecciona columnas numéricas para ver estadísticas")


if __name__ == "__main__":
    main()

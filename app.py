import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Set page config for a premium, wide-screen dashboard
st.set_page_config(
    page_title="Dashboard de Anuncios de Vehículos",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a beautiful, polished modern interface
st.markdown("""
<style>
    /* Google Fonts import */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    /* Font family overrides */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main title layout */
    .title-container {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 2.5rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    .title-container h1 {
        margin: 0;
        font-weight: 800;
        font-size: 2.5rem;
        letter-spacing: -0.05rem;
    }
    
    .title-container p {
        margin: 0.5rem 0 0 0;
        font-weight: 300;
        opacity: 0.9;
        font-size: 1.1rem;
    }
    
    /* Metric container styling */
    div[data-testid="metric-container"] {
        background-color: var(--secondary-background-color);
        border: 1px solid var(--border-color);
        padding: 1.25rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.25s ease, border-color 0.25s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-3px);
        border-color: #3B82F6;
    }

    /* Subheadings styling */
    h2, h3 {
        font-weight: 700;
        letter-spacing: -0.03rem;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to load dataset robustly
@st.cache_data
def load_data():
    csv_filename = "vehicles_us.csv"
    if os.path.exists(csv_filename):
        df = pd.read_csv(csv_filename)
    elif os.path.exists(os.path.join("notebooks", csv_filename)):
        df = pd.read_csv(os.path.join("notebooks", csv_filename))
    elif os.path.exists(os.path.join("..", csv_filename)):
        df = pd.read_csv(os.path.join("..", csv_filename))
    else:
        # Fallback to default absolute paths
        df = pd.read_csv("/home/betonorza/Documents/PYTHON/Vehiculos/vehicles_us.csv")
    
    # Preprocesamiento de datos
    df['model_year'] = df['model_year'].fillna(df.groupby('model')['model_year'].transform('median'))
    df['odometer'] = df['odometer'].fillna(df.groupby('model')['odometer'].transform('median'))
    
    # Fallback global por si algún modelo no tiene registros suficientes
    df['model_year'] = df['model_year'].fillna(df['model_year'].median()).astype(int)
    df['odometer'] = df['odometer'].fillna(df['odometer'].median()).astype(int)
    
    df['is_4wd'] = df['is_4wd'].fillna(0.0).astype(int)
    df['paint_color'] = df['paint_color'].fillna('desconocido')
    
    # Extraer fabricante
    df['manufacturer'] = df['model'].apply(lambda x: str(x).split()[0].title())
    df['model'] = df['model'].apply(lambda x: " ".join(str(x).split()[1:]).title())
    
    return df

# Load the data
try:
    df = load_data()
except Exception as e:
    st.error(f"Error al cargar el conjunto de datos: {e}")
    st.stop()

# Header Section
st.markdown("""
    <div class="title-container">
        <h1>🚗 Dashboard de Vehículos Usados</h1>
        <p>Análisis exploratorio interactivo de anuncios de ventas de coches en EE.UU.</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar filters
st.sidebar.markdown("### 🔍 Filtros de Búsqueda")

# Manufacturer filter
all_manufacturers = sorted(df['manufacturer'].unique())
selected_manufacturers = st.sidebar.multiselect(
    "Fabricante",
    options=all_manufacturers,
    default=[]
)

# Apply manufacturer filter to restrict available models in filter
if selected_manufacturers:
    filtered_by_manuf = df[df['manufacturer'].isin(selected_manufacturers)]
else:
    filtered_by_manuf = df

# Model filter
all_models = sorted(filtered_by_manuf['model'].unique())
selected_models = st.sidebar.multiselect(
    "Modelo de vehículo",
    options=all_models,
    default=[]
)

# Price range filter
min_price, max_price = int(df['price'].min()), int(df['price'].max())
selected_price = st.sidebar.slider(
    "Rango de Precio ($)",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, min_price + 50000)
)

# Odometer range filter
min_odo, max_odo = int(df['odometer'].min()), int(df['odometer'].max())
selected_odo = st.sidebar.slider(
    "Rango de Odómetro (millas)",
    min_value=min_odo,
    max_value=max_odo,
    value=(min_odo, 200000)
)

# Vehicle condition filter
all_conditions = sorted(df['condition'].unique())
selected_conditions = st.sidebar.multiselect(
    "Condición del vehículo",
    options=all_conditions,
    default=all_conditions
)

# Vehicle type filter
all_types = sorted(df['type'].unique())
selected_types = st.sidebar.multiselect(
    "Tipo de vehículo",
    options=all_types,
    default=all_types
)

# 4WD toggle
only_4wd = st.sidebar.checkbox("Mostrar solo vehículos 4WD (Tracción 4x4)")

# Apply filters to dataset
filtered_df = df.copy()

if selected_manufacturers:
    filtered_df = filtered_df[filtered_df['manufacturer'].isin(selected_manufacturers)]
if selected_models:
    filtered_df = filtered_df[filtered_df['model'].isin(selected_models)]
if selected_conditions:
    filtered_df = filtered_df[filtered_df['condition'].isin(selected_conditions)]
if selected_types:
    filtered_df = filtered_df[filtered_df['type'].isin(selected_types)]

filtered_df = filtered_df[
    (filtered_df['price'] >= selected_price[0]) & 
    (filtered_df['price'] <= selected_price[1]) &
    (filtered_df['odometer'] >= selected_odo[0]) & 
    (filtered_df['odometer'] <= selected_odo[1])
]

if only_4wd:
    filtered_df = filtered_df[filtered_df['is_4wd'] == 1]

# Display Metric KPI Cards
col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4)

with col_metric1:
    st.metric("Total Anuncios", f"{len(filtered_df):,}")
with col_metric2:
    avg_price = filtered_df['price'].mean() if len(filtered_df) > 0 else 0
    st.metric("Precio Promedio", f"${avg_price:,.0f}")
with col_metric3:
    avg_odo = filtered_df['odometer'].mean() if len(filtered_df) > 0 else 0
    st.metric("Kilometraje Promedio", f"{avg_odo:,.0f} mi")
with col_metric4:
    most_common_type = filtered_df['type'].mode()[0].title() if len(filtered_df) > 0 else "N/A"
    st.metric("Tipo más Popular", most_common_type)

st.markdown("---")

# Main content tabs
tab_charts, tab_advanced, tab_data = st.tabs([
    "📊 Gráficos Principales", 
    "📈 Análisis Avanzado", 
    "💾 Explorador de Datos"
])

with tab_charts:
    st.subheader("Visualización del Conjunto de Datos")
    
    # Challenge section with checkbox options to render plots
    col_cb1, col_cb2 = st.columns(2)
    with col_cb1:
        show_histogram = st.checkbox("Construir histograma", value=True, help="Marca esta casilla para visualizar el histograma")
    with col_cb2:
        show_scatter = st.checkbox("Construir gráfico de dispersión", value=True, help="Marca esta casilla para visualizar el gráfico de dispersión")
    
    # 1. Histogram
    if show_histogram:
        st.write("### Distribución del Kilometraje")
        st.write("Creación de un histograma para el conjunto de datos de anuncios de venta de coches.")
        
        # Select color grouping for histogram
        hist_color = st.selectbox(
            "Agrupar histograma por:",
            options=["condition", "transmission", "fuel", "type"],
            format_func=lambda x: {"condition": "Condición", "transmission": "Transmisión", "fuel": "Combustible", "type": "Tipo"}[x],
            key="hist_group"
        )
        
        if len(filtered_df) > 0:
            fig_hist = px.histogram(
                filtered_df, 
                x="odometer", 
                color=hist_color,
                title=f"Distribución del Odómetro por {hist_color.title()}",
                labels={"odometer": "Odómetro (millas)", "count": "Cantidad de anuncios", "condition": "Condición", "transmission": "Transmisión", "fuel": "Combustible", "type": "Tipo"},
                template="plotly_white",
                color_discrete_sequence=px.colors.qualitative.Safe,
                barmode="overlay"
            )
            fig_hist.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_hist, use_container_width=True)
        else:
            st.warning("No hay suficientes datos que coincidan con los filtros seleccionados.")
            
    # 2. Scatter Plot
    if show_scatter:
        st.write("### Relación entre Precio y Kilometraje")
        st.write("Creación de un gráfico de dispersión para el conjunto de datos de anuncios de venta de coches.")
        
        scatter_color = st.selectbox(
            "Agrupar gráfico de dispersión por:",
            options=["condition", "fuel", "transmission", "type"],
            format_func=lambda x: {"condition": "Condición", "fuel": "Combustible", "transmission": "Transmisión", "type": "Tipo"}[x],
            key="scatter_group"
        )
        
        if len(filtered_df) > 0:
            fig_scatter = px.scatter(
                filtered_df,
                x="odometer",
                y="price",
                color=scatter_color,
                title=f"Precio vs Odómetro por {scatter_color.title()}",
                labels={"odometer": "Odómetro (millas)", "price": "Precio ($)", "condition": "Condición", "fuel": "Combustible", "transmission": "Transmisión", "type": "Tipo"},
                template="plotly_white",
                opacity=0.6,
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            fig_scatter.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.warning("No hay suficientes datos que coincidan con los filtros seleccionados.")

with tab_advanced:
    st.subheader("Análisis de Precios y Tipos de Vehículos")
    
    col_adv1, col_adv2 = st.columns(2)
    
    with col_adv1:
        st.write("#### Precio Promedio por Tipo de Vehículo")
        if len(filtered_df) > 0:
            price_by_type = filtered_df.groupby("type")["price"].mean().reset_index().sort_values(by="price", ascending=False)
            fig_bar = px.bar(
                price_by_type,
                x="price",
                y="type",
                orientation="h",
                color="price",
                labels={"price": "Precio Promedio ($)", "type": "Tipo de Vehículo"},
                template="plotly_white",
                color_continuous_scale="Viridis"
            )
            fig_bar.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.warning("Sin datos.")
            
    with col_adv2:
        st.write("#### Distribución de Precios por Condición")
        if len(filtered_df) > 0:
            fig_box = px.box(
                filtered_df,
                x="condition",
                y="price",
                color="condition",
                labels={"condition": "Condición", "price": "Precio ($)"},
                template="plotly_white",
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            fig_box.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                showlegend=False
            )
            st.plotly_chart(fig_box, use_container_width=True)
        else:
            st.warning("Sin datos.")

with tab_data:
    st.subheader("Tabla de Datos y Descarga")
    st.write("Visualiza los datos filtrados y descárgalos en formato CSV.")
    
    show_raw = st.checkbox("Mostrar tabla de datos completos", value=False)
    if show_raw:
        st.dataframe(filtered_df, use_container_width=True)
    
    # Download CSV button
    if len(filtered_df) > 0:
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar Datos Filtrados como CSV",
            data=csv_data,
            file_name="vehiculos_filtrados.csv",
            mime="text/csv"
        )
    else:
        st.info("No hay datos disponibles para descargar.")
# 🚗 Dashboard de Análisis del Mercado de Vehículos Usados

Esta es una aplicación web interactiva desarrollada en **Streamlit** para analizar un conjunto de datos de anuncios de venta de coches en los Estados Unidos (`vehicles_us.csv`). El objetivo principal de este proyecto es aplicar buenas prácticas de desarrollo de software, incluyendo el uso de entornos virtuales, estructuración de proyectos, control de versiones con Git/GitHub y despliegue continuo en la nube (Render).

---

## 🌟 Características de la Aplicación

- **Filtros de Búsqueda Interactivos (Panel Lateral):**
  - Selección múltiple por **Fabricante** y **Modelo**.
  - Filtrado por **Rango de Precio** y **Kilometraje (Odómetro)** mediante controles deslizantes (sliders).
  - Filtrado por **Condición del Vehículo** (Excellent, Good, Fair, etc.) y **Tipo de Vehículo** (SUV, Sedan, Truck, etc.).
  - Filtro exclusivo para vehículos con tracción **4WD**.

- **Métricas Clave de Rendimiento (KPIs):**
  - Número total de anuncios que coinciden con los filtros.
  - Precio promedio de los coches listados.
  - Kilometraje promedio.
  - El tipo de carrocería más popular en la selección actual.

- **Visualizaciones Interactivas (Plotly Express):**
  - **Histograma de Kilometraje:** Muestra la distribución del odómetro con la opción de agrupar los datos dinámicamente por condición, transmisión, tipo de combustible, o tipo de vehículo.
  - **Gráfico de Dispersión (Precio vs Odómetro):** Permite analizar la relación entre el millaje y el costo de venta, con codificación de colores interactiva.
  - **Gráficos de Análisis Avanzado:**
    - Precio promedio por tipo de vehículo (gráfico de barras horizontales).
    - Distribución de precios por condición (diagramas de caja/boxplot).

- **Explorador y Descarga de Datos:**
  - Opción de visualizar la tabla completa de datos filtrados.
  - Botón para descargar la selección actual del conjunto de datos en formato **CSV**.

---

## 🛠️ Estructura del Proyecto

El repositorio sigue la siguiente estructura limpia de archivos:

```text
.
├── README.md              # Descripción del proyecto y guía de uso (este archivo)
├── app.py                 # Código principal de la aplicación Streamlit
├── requirements.txt       # Dependencias del proyecto
├── vehicles_us.csv        # Conjunto de datos principal
└── notebooks/
    └── EDA.ipynb          # Notebook de Jupyter con el análisis exploratorio de datos (EDA)
```

---

## 🚀 Instalación y Ejecución Local

### Paso 1. Clonar el repositorio
Clona este repositorio en tu máquina local:
```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_DIRECTORIO>
```

### Paso 2. Crear y activar el entorno virtual
Crea un entorno virtual (por ejemplo, llamado `vehicles_env`) e instálalo:
```bash
# Crear entorno virtual
python -m venv vehicles_env

# Activar entorno virtual (Linux/macOS)
source vehicles_env/bin/activate

# Activar entorno virtual (Windows)
vehicles_env\Scripts\activate
```

### Paso 3. Instalar dependencias
Instala los paquetes necesarios indicados en `requirements.txt`:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Paso 4. Ejecutar la aplicación
Ejecuta el servidor de desarrollo local de Streamlit:
```bash
streamlit run app.py
```
Abre en tu navegador la dirección URL que se muestra en la terminal (por defecto, `http://localhost:8501`).

---

## 🌐 Despliegue en Render

La versión en producción de esta aplicación está configurada para desplegarse automáticamente en **Render**:

1. **Build Command:**
   ```bash
   pip install --upgrade pip && pip install -r requirements.txt
   ```
2. **Start Command:**
   ```bash
   streamlit run app.py
   ```
3. **URL de producción:**
   https://`<APP_NAME>`.onrender.com/

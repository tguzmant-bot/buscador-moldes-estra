import streamlit as st
import pandas as pd
import io

# Configuración de la página (Título en la pestaña del navegador)
st.set_page_config(page_title="Localizador de Moldes ESTRA", page_icon="🚀")

# 1. BASE DE DATOS UNIFICADA (Pega aquí tus datos CSV tal cual)
data = """MOLDE,UBICACIÓN,FILA,PUESTO,NOTAS
MOL13736,H64-H76,1,1,Reubicación
MOL8187,H64-H76,2,1,Reubicación
MOL14319,H64-76,3,1,Reubicación
MOL14470,H64-H76,4,1,Reubicación
MOL13813,H64-H76,5,1,Reubicación
MOL15306,H64-H76,6,1,Reubicación
Z324,H64-H76,7,1,Reubicación
MOL15206,H64-H76,8,1,Reubicación
MOL13883,H64-H76,9,1,Reubicación
MOL13882,H64-H76,10,1,Reubicación
MOL15211,H64-H76,11,1,Reubicación
MOL15209,H64-H76,1,2,Reubicación
MOL15215,H64-H76,2,2,Reubicación
MOL15212,H64-H76,3,2,Reubicación
MOL15202,H64-H76,4,2,Reubicación
MOL15208,H64,5,2,Reubicación
MOL8721,H64-H76,6,2,Reubicación
MOL13725,H64-H76,7,2,Reubicación
MOL9786,H64-H76,8,2,Reubicación
MOL15222,H64-H76,9,2,Reubicación
MOL9782,H64-H76,10,2,Reubicación
MOL13733,H64-H76,11,2,Reubicación
MOL9883,H64-H76,1,3,Reubicación
MOL8422,H64-H76,2,3,Reubicación
MOL8965,H64-H76,3,3,Reubicación
MOL8961,H64,4,3,Reubicación
MOL3893,H64-H76,5,3,Reubicación
MOL15271,H64-H76,6,3,Reubicación
MOL14768,H64-H76,7,3,Reubicación
MOL7381,H64-H76,8,3,Reubicación
MOL15221,H64-H76,9,3,Reubicación
MOL15283,H64-H76,9,3,Reubicación
MOL4325,H64-H76,10,3,Reubicación
MOL15224,H64-H76,10,3,Reubicación
MOL4350,H64-H76,11,3,Reubicación
MOL15282,H64-H76,1,4,Reubicación
MOL15287,H64-H76,2,4,Reubicación
MOL15286,H64-H76,3,4,Reubicación
MOL15284,H64-H76,4,4,Reubicación
MOL8323,H64-H76,5,4,Reubicación
MOL6880,H64-H76,6,4,Reubicación
MOL14313,H64-H76,7,4,Reubicación
MOL9379,H64-H76,8,4,Reubicación
MOL4161,H64-H76,9,4,Reubicación
MOL3978,H64-H76,10,4,Reubicación
MOL9857,H64-H76,11,4,Reubicación
MOL13980,H75-H82,1,1,Reubicación
MOL13553,H75-H82,2,1,Reubicación
MOL8182,H82-H84,1,1,Reubicación
MOL15279,H82-H84,2,1,Reubicación
MOL13812,H82-H84,3,1,Reubicación
MOL13145,H82-H84,4,1,Reubicación
MOL13810,H82-H84,5,1,Reubicación
MOL14304,H82-H84,1,2,Reubicación
Z320,H82-H84,2,2,Reubicación
MOL14193,H82-H84,3,2,Reubicación
MOL15234,H82-H84,4,2,Reubicación
MOL6864,H82-H84,5,2,Reubicación
MOL8384,H84-H74,1,1,Reubicación
MOL742,H84-H74,2,1,Reubicación
MOL8722,H84-H74,3,1,Reubicación
MOL15213,H84-H74,4,1,Reubicación
MOL3990,H84-H74,1,2,Reubicación
MOL15288,H84-H74,2,2,Reubicación
MOL3955,H84-H74,3,2,Reubicación
MOL857,H84-H74,4,2,Reubicación
MOL3431,H74-H85,1,1,Reubicación
MOL15218,H74-H85,2,1,Reubicación
MOL15249,H74-H85,3,1,Reubicación
MOL15195,H74-H85,4,1,Reubicación
MOL15251,H74-H85,5,1,Reubicación
MOL15250,H74-H85,6,1,Reubicación
MOL14318,H74-H85,7,1,Reubicación
MOL15298,H74-H85,8,1,Reubicación
MOL600,H74-H85,9,1,Reubicación
MOL8363,H74-H85,10,1,Reubicación
MOL8966,H74-H85,1,2,Reubicación
MOL15199,H74-H85,2,2,Reubicación
MOL15205,H74-H85,3,2,Reubicación
MOL9433,H74-H85,4,2,Reubicación
MOL870,H74-H85,5,2,Reubicación
MOL15217,H74-H85,6,2,Reubicación
MOL15300,H74-H85,7,2,Reubicación
MOL836,H74-H85,8,2,Reubicación
MOL15254,H74-H85,9,2,Reubicación
MOL8962,H74-H85,10,2,Reubicación
MOL13729,H74-H85,1,3,Reubicación
MOL14731,H74-H85,2,3,Reubicación
MOL15305,H74-H85,3,3,Reubicación
MOL13814,H74-H85,2,3,Reubicación
MOL861,H74-H85,5,3,Reubicación
MOL15214,H74-H85,6,3,Reubicación
MOL15252,H74-H85,7,3,Reubicación
MOL15253,H74-H85,8,3,Reubicación
MOL3897,H74-H85,9,3,Reubicación
MOL15228,H74-H85,10,3,Reubicación
MOL15203,H74-H85,11,3,Reubicación
MOL15296,H74-H85,1,4,Reubicación
"""

# Cargar datos en Pandas
df = pd.read_csv(io.StringIO(data))

# 2. TÍTULOS Y ENCABEZADOS DE LA INTERFAZ
st.title("🚀 Sistema de Localización de Moldes")
st.subheader("Sector ZONA 1")
st.markdown("---") # Línea divisoria

# 3. COMPONENTES DE LA INTERFAZ
# Cuadro de texto para la búsqueda
codigo_input = st.text_input(
    label="🆔 MOLDE:",
    placeholder="Escriba el código (Ej: MOL13736)",
    help="Ingrese el código completo del molde"
)

# Botón de búsqueda
btn_buscar = st.button(
    label="🔍 BUSCAR UBICACIÓN",
    type="primary" # Lo hace resaltar en color azul por defecto en Streamlit
)

# 4. LÓGICA DE BÚSQUEDA
if btn_buscar or codigo_input: # Se ejecuta al dar clic o al dar Enter
    st.markdown("---") # Otra línea divisoria
    
    codigo = codigo_input.strip().upper()
    
    if not codigo:
        st.warning("⚠️ Por favor, ingrese un número de molde.")
    else:
        # Realizar la búsqueda en el DataFrame
        resultado = df[df['MOLDE'].str.upper() == codigo]
        
        if not resultado.empty:
            res = resultado.iloc[0]
            
            # Crear una tarjeta visual profesional para el resultado
            with st.container():
                st.success("📍 UBICACIÓN EN PLANTA ENCONTRADA")
                
                # Usar columnas para organizar la información
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="ESTANTERÍA", value=res['UBICACIÓN'])
                    st.metric(label="FILA", value=res['FILA'])
                with col2:
                    st.metric(label="PUESTO", value=res['PUESTO'])
                    st.write(f"**NOTAS:** {res['NOTAS']}")
                
                # CSS personalizado para darle el estilo verde de ESTRA
                st.markdown(
                    """
                    <style>
                    [data-testid="stMetricValue"] {
                        color: #28a745;
                        font-weight: bold;
                    }
                    div.stAlert {
                        border-left: 10px solid #28a745;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.error(f"""
                ❌ MOLDE NO ENCONTRADO
                El código "{codigo}" no existe en el sistema actual.
            """)

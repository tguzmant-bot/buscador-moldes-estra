import streamlit as st
import pandas as pd
import io

# Configuración de la página (Título en la pestaña del navegador, favicon y modo ancho)
st.set_page_config(page_title="Localizador de Moldes ESTRA", page_icon="🚀", layout="wide")

# 1. BASE DE DATOS UNIFICADA (Datos CSV originales tal cual)
# He mantenido tus datos originales, incluyendo los formatos mezclados (MOL, Z, solo número)
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
MOL15208,H64-H76,5,2,Reubicación
MOL8721,H64-H76,6,2,Reubicación
MOL13725,H64-H76,7,2,Reubicación
MOL9786,H64-H76,8,2,Reubicación
MOL15222,H64-H76,9,2,Reubicación
MOL9782,H64-H76,10,2,Reubicación
MOL13733,H64-H76,11,2,Reubicación
MOL9883,H64-H76,1,3,Reubicación
MOL8422,H64-H76,2,3,Reubicación
MOL8965,H64-H76,3,3,Reubicación
MOL8961,H64-H76,4,3,Reubicación
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
MOL8881,H75-H76,1,1,FILA IZQUIERDA AL LADO DE LA H75 Y ARRIBA DE ESTIBA 1
MOL588,H75-H76,1,2,FILA IZQUIERDA AL LADO DE LA H75 Y ARRIBA DE ESTIBA 1
MOL655,H75-H76,1,3,FILA IZQUIERDA AL LADO DE LA H75 Y ARRIBA DE ESTIBA 1
MOL13731,H75-H76,1,4,FILA IZQUIERDA AL LADO DE LA H75 Y ARRIBA DE ESTIBA 1
MOL712,H75-H76,1,5,FILA IZQUIERDA AL LADO DE LA H75 Y ARRIBA DE ESTIBA 1
MOL7961,H75-H76,1,1,AL LADO DE H75 Y ARRIBA DE ESTIBA 5
MOL7961,H75-H76,2,1,AL LADO DE H75 Y ARRIBA DE ESTIBA 5
MOL3904,H75-H76,1,1,ESTIBA 11
MOL13449,H75-H76,2,1,ESTIBA 11
MOL14454,H75-H76,1,2,ESTIBA 11
MOL14036,H75-H76,2,2,ESTIBA 11
MOL14597,H75-H76,1,3,ESTIBA 11
Z103,H75-H76,2,3,ESTIBA 11
MOL6862,H75-H76,2,1,FILA DERECHA AL LADO DE LA H75 Y ARRIBA DE ESTIBA 17
MOL3988,H75-H76,2,2,FILA DERECHA AL LADO DE LA H75 Y ARRIBA DE ESTIBA 17
MOL6381,H75-H76,2,3,FILA DERECHA AL LADO DE LA H75 Y ARRIBA DE ESTIBA 17
MOL6446,H75-H76,2,4,FILA DERECHA AL LADO DE LA H75 Y ARRIBA DE ESTIBA 17
MOL714,H75-H76,2,5,FILA DERECHA AL LADO DE LA H75 Y ARRIBA DE ESTIBA 17
Z98,H75-H76,2,6,FILA DERECHA AL LADO DE LA H75 Y ARRIBA DE ESTIBA 17
MOL14192,H75-H76,1,2,ESTIBA 22
MOL14455,H75-H76,2,1,ESTIBA 22
MOL7981,H75-H76,1,2,ESTIBA 22
MOL884,H75-H76,2,2,ESTIBA 22
MOL908,H75-H76,1,3,ESTIBA 22
MOL4329,H75-H76,2,3,ESTIBA 22
MOL14792,H75-H76,1,1,ESTIBA 5
MOL13447,H75-H76,2,1,ESTIBA 5
MOL9064,H75-H76,3,1,ESTIBA 5
MOL9225,H75-H76,1,2,ESTIBA 5
MOL13448,H75-H76,2,2,ESTIBA 5
MOL14748,H75-H76,3,2,ESTIBA 5
MOL14672,H75-H76,2,1,ESTIBA 12
MOL14090,H75-H76,3,1,ESTIBA 12
MOL13446,H75-H76,1,2,ESTIBA 12
MOL876,H75-H76,2,2,ESTIBA 12
MOL9065,H75-H76,3,2,ESTIBA 12
MOL3994,H75-H76,1,3,ESTIBA 12
MOL4327,H75-H76,2,3,ESTIBA 12
MOL3983,H75-H76,1,1,ESTIBA 17
MOL14347,H75-H76,1,2,ESTIBA 17
MOL3899,H75-H76,1,3,ESTIBA 17
MOL14303,H75-H76,2,1,ESTIBA 17
MOL14346,H75-H76,2,2,ESTIBA 17
MOL14769,H75-H76,2,3,ESTIBA 17
MOL4320,H75-H76,2,4,Debajo de las estiba 17
MOL3901,H75-H76,1,1,ESTIBA 6
MOL13148,H75-H76,1,2,ESTIBA 6
Z324-2,H75-H76,1,3,ESTIBA 6
MOL14576,H75-H76,2,1,ESTIBA 6
MOL9732,H75-H76,2,2,ESTIBA 6
MOL13450,H75-H76,2,3,ESTIBA 6
MOL4332,H75-H76,1,1,ESTIBA 1
MOL13133,H75-H76,2,1,ESTIBA 1
Z161,H75-H76,3,1,ESTIBA 1
MOL8724,H75-H76,1,2,ESTIBA 1
MOL6885,H75-H76,2,2,ESTIBA 1
MOL4349,H75-H76,3,2,ESTIBA 1
MOL14082,H75-H76,1,1,ESTIBA 2
MOL602,H75-H76,1,2,ESTIBA 2
Z162,H75-H76,1,3,ESTIBA 2
MOL4346,H75-H76,2,1,ESTIBA 2
MOL3898,H75-H76,2,2,ESTIBA 2
MOL4324,H75-H76,1,1,ESTIBA 3
MOL3948,H75-H76,1,2,ESTIBA 3
MOL4344,H75-H76,1,3,ESTIBA 3
MOL4160,H75-H76,2,1,ESTIBA 3
MOL7122,H75-H76,2,2,ESTIBA 3
MOL14083,H75-H76,2,3,ESTIBA 3
MOL655,H75-H76,1,1,ESTIBA 4
MOL13861,H75-H76,2,1,ESTIBA 4
MOL8968,H75-H76,1,2,ESTIBA 4
MOL4347,H75-H76,2,2,ESTIBA 4
MOL15262,H75-H76,3,2,ESTIBA 4
MOL4348,H75-H76,1,1,ESTIBA 7
MOL4165,H75-H76,1,2,ESTIBA 7
MOL7323,H75-H76,1,3,ESTIBA 7
MOL7123,H75-H76,2,1,ESTIBA 7
MOL13734,H75-H76,2,2,ESTIBA 7
MOL4317,H75-H76,2,3,ESTIBA 7
MOL9812,H75-H76,1,1,ESTIBA 8
MOL590,H75-H76,2,1,ESTIBA 8
MOL8322,H75-H76,1,2,ESTIBA 8
MOL4339,H75-H76,2,2,ESTIBA 8
MOL7961,H75-H76,3,2,ESTIBA 8
MOL14716,H75-H76,1,1,ESTIBA 9
MOL709,H75-H76,1,2,ESTIBA 9
MOL13622,H75-H76,2,1,ESTIBA 9
MOL6882,H75-H76,2,2,ESTIBA 9
MOL872,H75-H76,2,3,ESTIBA 9
MOL14791,H75-H76,3,3,ESTIBA 9
Z276,H75-H76,1,1,ESTIBA 10
MOL15263,H75-H76,1,2,ESTIBA 10
MOL15261,H75-H76,1,3,ESTIBA 10
MOL13863,H75-H76,2,1,ESTIBA 10
MOL7441,H75-H76,2,2,ESTIBA 10
MOL15264,H75-H76,2,3,ESTIBA 10
MOL4143,H75-H76,1,1,ESTIBA 13
MOL706,H75-H76,1,2,ESTIBA 13
MOL8964,H75-H76,1,3,ESTIBA 13
MOL15223,H75-H76,2,1,ESTIBA 13
MOL9858,H75-H76,2,1,ESTIBA 13
MOL4323,H75-H76,1,1,ESTIBA 14
MOL4341,H75-H76,1,2,ESTIBA 14
MOL8081,H75-H76,1,3,ESTIBA 14
MOL13118,H75-H76,2,2,ESTIBA 14
MOL4340,H75-H76,2,3,ESTIBA 14
MOL8185,H75-H76,1,1,ESTIBA 15
MOL6893,H75-H76,1,2,ESTIBA 15
MOL14037,H75-H76,1,3,ESTIBA 15	
MOL9794,H75-H76,2,2,ESTIBA 15
MOL4289,H75-H76,1,1,ESTIBA 16
MOL4169,H75-H76,1,2,ESTIBA 16
MOL9791,H75-H76,1,3,ESTIBA 16
MOL215727,H75-H76,2,1,ESTIBA 16
MOL13867,H75-H76,2,2,ESTIBA 16
MOL13864,H75-H76,2,3,ESTIBA 16
MOL4320,H75-H76,1,1,ESTIBA 18
MOL6348,H75-H76,2,1,ESTIBA 18
MOL625,H75-H76,1,2,ESTIBA 18
MOL4318,H75-H76,2,2,ESTIBA 18
MOL9434,H75-H76,3,2,ESTIBA 18
MOL14086,H75-H76,1,1,ESTIBA 19
MOL13739,H75-H76,1,2,ESTIBA 19
MOL761,H75-H76,1,3,ESTIBA 19
MOL3987,H75-H76,2,1,ESTIBA 19
MOLZ173,H75-H76,2,2,ESTIBA 19
MOL14671,H75-H76,1,1,ESTIBA 20
MOL8421,H75-H76,1,2,ESTIBA 20
MOL7863,H75-H76,2,1,ESTIBA 20
MOL716,H75-H76,2,2,ESTIBA 20
Z324-1,H75-H76,1,1,ESTIBA 21
MOL14091,H75-H76,1,2,ESTIBA 21
MOL13868,H75-H76,1,3,ESTIBA 21
MOL3997,H75-H76,2,1,ESTIBA 21
MOL14089,H75-H76,2,2,ESTIBA 21
MOL13303,H75-H76,2,3,ESTIBA 21
MOL646,H75-H76,3,2,ESTIBA 21
MOL14085,H75-H76,3,3,ESTIBA 21
MOL4328,H75-H76,1,1,ESTIBA 23
MOL4326,H75-H76,1,2,ESTIBA 23
MOL718,H75-H76,2,1,ESTIBA 23
MOL14087,H75-H76,2,2,ESTIBA 23
MOL4286,H75-H76,1,1,ESTIBA 24
15434,H75-H76,1,2,ESTIBA 24
MOL4331,H75-H76,1,3,ESTIBA 24
MOL15299,H75-H76,2,1,ESTIBA 24
MOL4287,H75-H76,2,2,ESTIBA 24
MOL4342,H75-H76,2,3,ESTIBA 24
MOL14191,H75-H76,1,1,ESTIBA 25
MOL14756,H75-H76,1,2,ESTIBA 25
MOL14088,H75-H76,1,3,ESTIBA 25
MOL13872,H75-H76,2,1,ESTIBA 25
MOL15204,H75-H76,2,2,ESTIBA 25
MOL892,H75-H76,2,3,ESTIBA 25
MOL4333,H75-H76,1,1,ESTIBA 26
MOL14345,H75-H76,1,2,ESTIBA 26
MOL13472,H75-H76,1,3,ESTIBA 26
MOL6886,H75-H76,2,1,ESTIBA 26
MOL8082,H75-H76,2,2,ESTIBA 26
MOL13730,H75-H76,2,3,ESTIBA 26
"""

# Cargar datos originales en Pandas
df = pd.read_csv(io.StringIO(data))

# --- SECCIÓN DE LIMPIEZA DE DATOS (Interna) ---
# Usamos regex para borrar "MOL" o "Z" (mayúsculas o minúsculas) de la columna 'MOLDE'
# case=False para ignorar diferencias entre MOL/mol o Z/z.
# regex=True para usar expresiones regulares.
# r'(MOL|Z)' significa "buscar la cadena MOL O buscar la letra Z".
df['MOLDE'] = df['MOLDE'].str.replace(r'(MOL|Z)', '', case=False, regex=True)

# 2. TÍTULOS Y ENCABEZADOS DE LA INTERFAZ
# Centramos el título profesional para que se vea más profesional en modo "wide"
st.markdown("<h1 style='text-align: center; color: #2c3e50;'>🚀 Sistema de Localización de Moldes</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #7f8c8d;'>Sector ZONA 1</h3>", unsafe_allow_html=True)
st.markdown("---") # Línea divisoria

# 3. COMPONENTES DE LA INTERFAZ
# Centramos el buscador usando columnas
col_left, col_mid, col_right = st.columns([1, 2, 1])

with col_mid:
    # Cuadro de texto para la búsqueda
    codigo_input = st.text_input(
        label="🆔 MOLDE:",
        # --- ACTUALIZADO: Texto de ayuda para el operario ---
        placeholder="Escriba el número (Ej: 13736 o 324)",
        help="Ingrese el número del molde, puede escribir 'MOL', 'Z', minúsculas o solo el código numérico"
    )

    # Botón de búsqueda centrado internamente
    col_btn_l, col_btn_m, col_btn_r = st.columns([1, 2, 1])
    with col_btn_m:
        btn_buscar = st.button(
            label="🔍 BUSCAR UBICACIÓN",
            type="primary", # Botón azul resaltado
            use_container_width=True # Ocupa todo el ancho de su columna
        )

# 4. LÓGICA DE BÚSQUEDA
if btn_buscar or (codigo_input and not codigo_input.isspace()): # Se ejecuta al dar clic o al dar Enter
    st.markdown("---") # Otra línea divisoria
    
    # --- AQUÍ ESTÁ EL CAMBIO CLAVE PARA BORRAR MOL O Z INDEPENDIENTE DEL CASO ---
    # Limpiamos la entrada del operario antes de buscar
    # Primero quitamos espacios extras y lo pasamos a mayúsculas
    entrada_limpia = codigo_input.strip().upper()
    
    # Ahora borramos "MOL" o "Z" de lo que el técnico escribió de forma manual y robusta
    # Primero verificamos que no esté vacío el input limpio
    if entrada_limpia:
        # Usamos una variable intermedia para la limpieza del input
        codigo_limpio_input = entrada_limpia
        # Si la entrada contiene 'MOL', lo borramos. Al ya estar en mayúsculas, 'MOL' == 'mol'.str.upper()
        if 'MOL' in entrada_limpia:
            codigo_limpio_input = entrada_limpia.replace('MOL', '')
        # Si la entrada contiene 'Z', la borramos. Al ya estar en mayúsculas, 'Z' == 'z'.str.upper()
        elif 'Z' in entrada_limpia:
            codigo_limpio_input = entrada_limpia.replace('Z', '')
        # Si no tiene MOL ni Z, codigo_limpio_input ya es igual a entrada_limpia

        # Realizar la búsqueda en el DataFrame (que ya está limpio internamente)
        resultado = df[df['MOLDE'] == codigo_limpio_input]
        
        if not resultado.empty:
            res = resultado.iloc[0]
            
            # Usamos columnas laterales vacías para centrar el resultado profesionalmente
            r_left, r_mid, r_right = st.columns([1, 4, 1])
            
            with r_mid:
                # Crear una tarjeta visual profesional para el resultado
                with st.container():
                    st.success(f"📍 UBICACIÓN EN PLANTA ENCONTRADA PARA EL MOLDE: {codigo_limpio_input}")
                    
                    # --- ESTA ES LA PARTE CLAVE PARA IGUALAR EL TAMAÑO DE LAS NOTAS ---
                    # Organizamos la información en métricas profesionales
                    col_met1, col_met2, col_met3 = st.columns(3)
                    with col_met1:
                        st.metric(label="UBICACIÓN / ESTANTERÍA", value=res['UBICACIÓN'])
                    with col_met2:
                        st.metric(label="FILA", value=res['FILA'])
                    with col_met3:
                        st.metric(label="PUESTO", value=res['PUESTO'])
                    
                    # Ahora creamos una "métrica" personalizada para las notas usando HTML/CSS
                    # Esto replica el aspecto visual de las métricas (fondo, bordes, fuente grande)
                    html_notas = f"""
                    <div style="
                        background-color: white;
                        border-left: 10px solid #28a745;
                        border-radius: 8px;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                        padding: 20px;
                        margin-top: 20px;
                    ">
                        <div style="
                            font-family: sans-serif;
                            font-size: 14px;
                            font-weight: bold;
                            color: #555;
                            text-transform: uppercase;
                            margin-bottom: 8px;
                        ">
                            NOTAS IMPORTANTES
                        </div>
                        <div style="
                            font-family: 'Segoe UI', sans-serif;
                            font-size: 36px;
                            font-weight: 700;
                            color: #000;
                            line-height: 1.2;
                        ">
                            {res['NOTAS']}
                        </div>
                    </div>
                    """
                    st.markdown(html_notas, unsafe_allow_html=True)
                    
                    # CSS personalizado adicional para darle el estilo verde de ESTRA a las métricas nativas
                    st.markdown(
                        """
                        <style>
                        [data-testid="stMetricValue"] {
                            color: #28a745;
                            font-weight: bold;
                        }
                        /* Cambiar color de fondo del alert de éxito para que sea verde ESTRA */
                        div[data-testid="stAlertSucces"] {
                            border-left: 10px solid #28a745;
                        }
                        </style>
                        """,
                        unsafe_allow_html=True
                    )
        else:
            st.error(f"""
                ❌ MOLDE NO ENCONTRADO
                El código "{codigo_limpio_input}" no existe en el sistema actual de la ZONA 1.
            """)
    else:
        st.warning("⚠️ Por favor, ingrese un número de molde antes de buscar.")

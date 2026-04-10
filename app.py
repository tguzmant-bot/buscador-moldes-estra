import streamlit as st
import pandas as pd 
import io

# Configuración de la página (Título en la pestaña del navegador, favicon y modo ancho)
st.set_page_config(page_title="Localizador de Moldes ESTRA", page_icon="🚀", layout="wide")

# 1. BASE DE DATOS UNIFICADA (Datos CSV originales tal cual)
# He mantenido tus datos originales, incluyendo los formatos mezclados (MOL, Z, solo número)
data = """MOLDE,UBICACIÓN,FILA,PUESTO,NOTAS
MOL13736,H64-H76,1,1,HIELERA 3L			
MOL8187,H64-H76,2,1,Reubicación
MOL14319,H64-76,3,1,ESTRAPACK 1 LITRO			
MOL14470,H64-H76,4,1,TAPA RECIPIENTE OCA RECTANGULAR 2.2L			
MOL13813,H64-H76,5,1,BASE LOCKER			
MOL15306,H64-H76,6,1,CUERPO 19L			
Z324,H64-H76,7,1,MACETA			
MOL15206,H64-H76,8,1,ARO PAPELERA VAIVEN BINS 26L			 
MOL13883,H64-H76,9,1,CUERPO ESTRAPACK ALTO - 3 L			
MOL13882,H64-H76,10,1,CUERPO ESTRAPACK ALTO - 1.5 L			
MOL15211,H64-H76,11,1,SUJETADOR DE BOLSA DOBLE 53L			
MOL15209,H64-H76,1,2,ARO PAPELERA VAIVEN BINS 53L			
MOL15215,H64-H76,2,2,TAPA CANECA PEDAL BINS 22L			
MOL15212,H64-H76,3,2,TAPA CANECA PEDAL BINS 10L			
MOL15202,H64-H76,4,2,TAPA PAPELERA VAIVEN BINS 10L			
MOL15208,H64-H76,5,2,TAPA PAPELERA VAIVEN BINS 53L			
MOL8721,H64-H76,6,2,CUERPO PAPELERA DE PEDAL 10 L			
MOL13725,H64-H76,7,2,PLATO ANTIDESPERDICIO			
MOL9786,H64-H76,8,2,BALDE CON ESCURRIDOR - BALDE			
MOL15222,H64-H76,9,2,BANDEJA MULTIBOX			
MOL9782,H64-H76,10,2,PONCHERA CUADRADA No. 4			
MOL13733,H64-H76,11,2,TAPA CANASTA ROPA C/TAPA			
MOL9883,H64-H76,1,3,JARRA 2.5 L LINEA ACQUA			
MOL8422,H64-H76,2,3,CUERPO PAPELERA VAIVEN 10 L			
MOL8965,H64-H76,3,3,EXTERIOR TERMO 8 L			
MOL8961,H64-H76,4,3,EXTERIOR TERMO 4 L			
MOL3893,H64-H76,5,3,MUG 10 ONZAS			
MOL15271,H64-H76,6,3,Reubicación
MOL14768,H64-H76,7,3,CUERPO JARRA BASICA 2L			
MOL7381,H64-H76,8,3,PAPELERA PERFORADA 8 L			
MOL15221,H64-H76,9,3,TARRO FLOTADOR			
MOL15283,H64-H76,9,3,SUJETADOR CANECA 5 L			
MOL4325,H64-H76,10,3,INTERIOR NEVERA PERSONAL 4.5 L			
MOL15224,H64-H76,10,3,RECIPIENTE 2L MULTIBOX			
MOL4350,H64-H76,11,3,TAPA ESTRAPACK REDONDO # 7 - 7.5 L			
MOL15282,H64-H76,1,4,TAPA CANECA PEDAL BINS 5 L			
MOL15287,H64-H76,2,4,TAPA CAJA ORGANIZADORA 4L			
MOL15286,H64-H76,3,4,CAJA ORGANIZADORA 4L			
MOL15284,H64-H76,4,4,PEDAL CANECA 5L			
MOL8323,H64-H76,5,4,ARO PAPELERA 35 L			
MOL6880,H64-H76,6,4,CUERPO ESCURRIDOR DE PLATOS			
MOL14313,H64-H76,7,4,CUERPO EXTERNO NEVERA 22 L			
MOL9379,H64-H76,8,4,GABINETE DE BAÑO N°3 - PUERTA LATERAL			
MOL4161,H64-H76,9,4,JARRA C/MEZCL.1.5 LT.CUERPO			
MOL3978,H64-H76,10,4,BALDE C/ESCURRIDOR-ESCURRIDOR			
MOL9857,H64-H76,11,4,CUERPO BALDE ECONOMICO			
MOL15227,H75-H82,1,1,EXTERIOR NEVERA 10L			
MOL13980,H75-H82,2,1,PIPETA (nuevo)			
MOL13553,H75-H82,3,1,BASE INFERIOR SOPORTE BRIDA.			
MOL8182,H82-H84,1,1,TAPA CAJA ORGANIZADORA 16 LITROS			
MOL15279,H82-H84,2,1,BROCHE CAJA ORGANIZADORA 2021						
MOL13812,H82-H84,3,1,MODULO POSTERIOR LOCKER			
MOL13145,H82-H84,4,1,PAPELERA DE PEDAL 20L -TAPA			
MOL13810,H82-H84,5,1,MODULO HORIZONTAL LOCKER			
MOL14304,H82-H84,1,2,PUERTA LOCKER 300			
Z320,H82-H84,2,2,Porta equipaje			
MOL14193,H82-H84,3,2,ENTREPAÑO LOCKER			
MOL15234,H82-H84,4,2,Reubicación
MOL6864,H82-H84,5,2,MANIJA ESTRABALDE MULTIUSOS			
MOL8384,H84-H74,1,1,ARO PAPELERA VAIVEN 10 L			
MOL742,H84-H74,2,1,MUG 14 ONZAS			
MOL8722,H84-H74,3,1,TAPA PAPELERA DE PEDAL 10 L			
MOL15213,H84-H74,4,1,SUJETADOR BOLSA CANECA PEDAL BINS 10L			
MOL3990,H84-H74,1,2,PAPEL. PED.SLIM 42 LT PALANCA			
MOL15288,H84-H74,2,2,ARO PAPELERA VAIVEN CLASICA 35-53L			
MOL3955,H84-H74,3,2,Reubicación
MOL857,H84-H74,4,2,TAPA P.REF.101/2/3/23 A 37/47			
MOL3431,H74-H85,1,1,MUNDIMOLD C131 60X40X25 FLL-LOGO ALPINA			
MOL15218,H74-H85,2,1,TAPA CANECA PEDAL BINS 44L			
MOL15249,H74-H85,3,1,TAPA CAJONERA GRANDE			
MOL15195,H74-H85,4,1,SEÑAL DE PREVENCIÓN			
MOL15251,H74-H85,5,1,BASE Y PARALES CAJONERA GRANDE			
MOL15250,H74-H85,6,1,CAJON CAJONERA GRANDE			
MOL14318,H74-H85,7,1,MANIJA CANASTA SUPERMERCADO			
MOL15298,H74-H85,8,1,CUERPO 6L			
MOL600,H74-H85,9,1,BANDEJA PEQUENA			
MOL8363,H74-H85,10,1,TAPA VAIVÉN CONTENEDOR 121 L			
MOL8966,H74-H85,1,2,INTERIOR TERMO 8 L			
MOL15199,H74-H85,2,2,CUERPO CANECA PEDAL BINS 10L			
MOL15205,H74-H85,3,2,TAPA PAPELERA VAIVEN BINS 26L			
MOL9433,H74-H85,4,2,PUERTA GABINETE DE BAÑO # 4			
MOL870,H74-H85,5,2,COMEDERO PARA POLLOS BEBE			
MOL15217,H74-H85,6,2,PEDAL CANECA BINS 22L			
MOL15300,H74-H85,7,2,CUERPO 5L			
MOL836,H74-H85,8,2,RECOLECTOR DE CAFE			
MOL15254,H74-H85,9,2,BASE CAJONERA PEQUEÑA			
MOL8962,H74-H85,10,2,INTERIOR TERMO 4 L			
MOL13729,H74-H85,1,3,TAPA CANECA 37 L			
MOL14731,H74-H85,2,3,Reubicación
MOL15305,H74-H85,3,3,CUERPO 11L			
MOL13814,H74-H85,2,3,PUERTA LOCKER			
MOL861,H74-H85,5,3,DIVISION 60/40 CMS. PARA CAJA			
MOL15214,H74-H85,6,3,PEDAL CANECA BINS 10L			
MOL15252,H74-H85,7,3,TAPA CAJONERA PEQUEÑA			
MOL15253,H74-H85,8,3,CAJON CAJONERA PEQUEÑA			
MOL3897,H74-H85,9,3,TAPA Y BASE LONCHERA			
MOL15228,H74-H85,10,3,INTERIOR NEVERA 10L			
MOL15203,H74-H85,11,3,ARO PAPELERA VAIVEN BINS10L			
MOL15296,H74-H85,1,4,CAJA 60 X 40 X 18			
MOL6344,Sopladora 2,1,1,NEVERA FAMILIAR 42 L - TAPA			
MOL13230, Sopladora 2,1,2,Reubicación
MOL8881,Frente Estan 1,1,1,ESTIBA 
MOL588,Frente Estan 1,1,2,ESTIBA 
MOL655,Frente Estan 1,1,3,ESTIBA 
MOL13731,Frente Estan 1,1,4,ESTIBA 
MOL712,Frente Estan 1,1,5,ESTIBA 
MOL3904,Sopladora 2,1,1,ESTIBA 11
MOL13449,Sopladora 2,2,1,ESTIBA 11
MOL14454,Sopladora 2,1,2,ESTIBA 11
MOL14036,Sopladora 2,2,2,ESTIBA 11
MOL14597,Sopladora 2,1,3,ESTIBA 11
Z103,Sopladora 2,2,3,ESTIBA 11
MOL6862,H75-H76,2,1,FILA DERECHA AL LADO DE LA H75 Y ARRIBA DE ESTIBA 17
MOL3988,H75-H76,2,2,FILA DERECHA AL LADO DE LA H75 Y ARRIBA DE ESTIBA 17
MOL6381,H75-H76,2,3,FILA DERECHA AL LADO DE LA H75 Y ARRIBA DE ESTIBA 17
MOL6446,ESTANTERÍA 1,1,1,VASO 8 ONZAS			
MOL714,H75-H76,2,5,FILA DERECHA AL LADO DE LA H75 Y ARRIBA DE ESTIBA 17
Z98,H75-H76,2,6,FILA DERECHA AL LADO DE LA H75 Y ARRIBA DE ESTIBA 17
MOL14192,ESTANTERÍA 1,1,3,ELEMENTOS DE UNIÓN LOCKER			
MOL14455,ESTANTERÍA 1,1,3,TORNILLO TUERCA LOCKER			
MOL7981,ESTANTERÍA 1,1,3,TAPA ESTRAPACK RECTANGULAR 0.35 LITROS			
MOL884,ESTANTERÍA 1,1,3,TORPEDO HUACAL			
MOL908,ESTANTERÍA 1,2,1,VARILLA CENTRAL COMEDERO 12 k			
MOL4329,ESTANTERÍA 1,1,3,TAPA ESTRAPACK REDONDO # 4 - 2 L			
MOL14792,S1-S2,1,1,ESTIBA 5
MOL13447,S1-S2,2,1,ESTIBA 5
MOL9064,S1-S2,3,1,ESTIBA 5
MOL9225,S1-S2,1,2,ESTIBA 5
MOL13448,S1-S2,2,2,ESTIBA 5
MOL14748,S1-S2,3,2,ESTIBA 5
MOL14672,ESTANTERÍA 1,5,3,TAPA ESTRAPACK #2			
MOL14090,ESTANTERÍA 1,5,3,TAPA RECIPIENTE CUADRADO NEVERA 0.5L			
MOL13446,ESTANTERÍA 1,5,3,GUARDIÁN 1.3L - CUERPO			
MOL876,ESTANTERÍA 1,5,3,PIN VALVULA			
MOL9065,ESTANTERÍA 1,5,3,BANDEJA ESTRAPACK CARNES Y VERDURAS 4L			
MOL3994,H75-H76,1,3,ESTIBA 12
MOL4327,ESTANTERÍA 1,4,3,TAPA ESTRAPACK REDONDO # 3 - 1 L			
MOL3983,H73-S1,1,1,ESTIBA 17
MOL14347,H73-S1,1,2,ESTIBA 17
MOL3899,H73-S1,1,3,ESTIBA 17
MOL14303,H73-S1,2,1,ESTIBA 17
MOL14346,H73-S1,2,2,ESTIBA 17
MOL14769,H73-S1,2,3,ESTIBA 17
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
MOL14082,Frente Estan 1,1,1,ESTIBA 2
MOL602,Frente Estan 1,1,2,ESTIBA 2
Z162,Frente Estan 1,1,3,ESTIBA 2
MOL4346,Frente Estan 1,2,1,ESTIBA 2
MOL3898,Frente Estan 1,2,2,ESTIBA 2
MOL4324,Sopladora 2,1,1,ESTIBA 3
MOL3948,Sopladora 2,1,2,ESTIBA 3
MOL4344,Sopladora 2,1,3,ESTIBA 3
MOL4160,Sopladora 2,2,1,ESTIBA 3
MOL7122,Sopladora 2,2,2,ESTIBA 3
MOL14083,ESTANTERÍA 1,4,3,RECIPIENTE RECTANGULAR DESPENSA 3L			
MOL655,Frente Estan 1,1,1,ESTIBA 4
MOL13861,Frente Estan 1,2,1,ESTIBA 4
MOL8968,Frente Estan 1,1,2,ESTIBA 4
MOL4347,Frente Estan 1,2,2,ESTIBA 4
MOL15262,Frente Estan 1,3,2,ESTIBA 4
MOL4348,H73-S1,1,1,ESTIBA 7
MOL4165,H73-S1,1,2,ESTIBA 7
MOL7323,H73-S1,1,3,ESTIBA 7
MOL7123,H73-S1,2,1,ESTIBA 7
MOL13734,H73-S1,2,2,ESTIBA 7
MOL4317,H73-S1,2,3,ESTIBA 7
MOL9812,Frente Estan 1,1,1,ESTIBA 8
MOL590,Frente Estan 1,2,1,ESTIBA 8
MOL8322,Frente Estan 1,1,2,ESTIBA 8
MOL4339,Frente Estan 1,2,2,ESTIBA 8
MOL7961,Frente Estan 1,3,2,ESTIBA 8
MOL14716,H75-H76,1,1,ESTIBA 9
MOL709,ESTANTERÍA 1,4,1,Cuerpo Tazon Estracook 1.5 L			
MOL13622,ESTANTERÍA 1,4,2,CUERPO ESTRAPACK #4			
MOL6882,ESTANTERÍA 1,5,2,EXTERIOR TERMO 1 LITRO			
MOL872,ESTANTERÍA 1,3,2,BOTELLA PARA BEBEDERO DE GALON			
MOL14791,ESTANTERÍA 1,5,1,BROCHE CAJA ORGANIZADORA DECO			
Z276,ESTANTERÍA 1,4,3,CUBO ROSAS			
MOL15263,ESTANTERÍA 1,3,3,MARCO Y PUERTA GARAGE			
MOL15261,H75-H76,1,3,ESTIBA 10
MOL13863,ESTANTERÍA 1,3,3,CUERPO OCA RECTANGULAR 1.2 LITROS			
MOL7441,ESTANTERÍA 1,4,3,CAJA SOUVENIR ECONOMI-K			
MOL15264,ESTANTERÍA 1,2,2,CABALLETES			
MOL4143,H75-H76,1,1,ESTIBA 13
MOL706,Frente Estan 1,1,2,ESTIBA 13
MOL8964,Frente Estan 1,1,3,ESTIBA 13
MOL15223,Frente Estan 1,2,1,ESTIBA 13
MOL9858,Frente Estan 1,2,1,ESTIBA 13
MOL4323,ESTANTERÍA 1,3,1,MANIJA NEVERA PERSONAL 45 L			
MOL4341,H75-H76,1,2,ESTANTERÍA 1 
MOL8081,ESTANTERÍA 1,3,2,JARRA MEDIDORA 1 L			
MOL13118,ESTANTERÍA 1,4,1,VASO 10 ONZ SAN - ACRILICO			
MOL4340,ESTANTERÍA 1,1,2,CUERPO ESTRAPACK CUADRADO 2.5 L			
MOL8185,ESTANTERÍA 1,1,1,N/A
MOL6893,ESTANTERÍA 1,1,2,N/A
MOL14037,ESTANTERÍA 1,5,2,CUERPO PLATO DIVIDIDO 1.4L				
MOL9794,ESTANTERÍA 1,4,1,PLATO SOPA NO. 2			
MOL4289,Frente Estan 1,1,1,ESTIBA 16
MOL4169,ESTANTERÍA 1,3,2,CHAZO FILTRAFACIL AVANZADO			
MOL9791,ESTANTERÍA 1,3,2,CUBETA PARA HIELO			
MOL215727,Frente Estan 1,2,1,ESTIBA 16
MOL13867,ESTANTERÍA 1,3,3,CUERPO OCA CUADRADO 2.3 LITROS			
MOL13864,ESTANTERÍA 1,3,2,TAPA OCA RECTANGULAR 1.2 LITROS			
MOL4320,H75-H76,1,1,CUERPO ESTRAPACK RECTANGULAR # 4 - 4 L			
MOL6348,ESTANTERÍA 1,1,2,SOPORTE PAPELERA ESTRASLIM 42 L			
MOL625,ESTANTERÍA 1,4,1,TAZA GRANDE			
MOL4318,H75-H76,2,2,CUERPO ESTRAPACK RECTANGULAR # 3 - 2 L			
MOL9434,ESTANTERÍA 1,2,1,SOPORTE ESPEJO GABINETE DE BAÑO # 4.			
MOL14086,ESTANTERÍA 1,2,3,RECIPIENTE RECTANGULAR DESPENSA 3L BAJO			
MOL13739,ESTANTERÍA 1,3,1,VASO  15 oz			
MOL761,ESTANTERÍA 1,4,2,BASE LOCKER			
MOL3987,ESTANTERÍA 1,3,1,CUERPO ESTRAPACK REDONDO # 5 - 3.25 L			
MOLZ173,ESTANTERÍA 1,2,3,RP5 TAPA SUPERIOR			
MOL14671,H75-H76,1,1,TAPA ESTRAPACK #1			
MOL8421,ESTANTERÍA 1,2,1,TAPA PAPELERA VAIVEN 10 L			
MOL7863,ESTANTERÍA 1,2,2,AJUSTADOR NIVEL NUEVO			
MOL716,ESTANTERÍA 1,3,2,JARRA ESTRAPREMIER 2 LITROS TAPA MEZCLADOR			
Z324-1,H75-H76,1,1,ESTIBA 21
MOL14091,ESTANTERÍA 1,5,2,RECIPIENTE RECTANGULAR DESPENSA 1L			
MOL13868,ESTANTERÍA 1,5,1,TAPA OCA CUADRADO 2.3 LITROS			 
MOL3997,Frente Estan 1,2,1,ESTIBA 21
MOL14089,ESTANTERÍA 1,5,2,RECIPIENTE CUADRADO NEVERA 0.75L			
MOL13303,ESTANTERÍA 1,2,3,N/A
MOL646,Frente Estan 1,3,2,ESTIBA 21
MOL14085,ESTANTERÍA 1,4,2,TAPA RECIPIENTE RECTANGULAR NEVERA 0.5L			
MOL4328,ESTANTERÍA 1,1,1,CUERPO ESTRAPACK REDONDO # 4 - 2 L			
MOL4326,ESTANTERÍA 1,1,1,CUERPO ESTRAPACK REDONDO # 3 - 1 L			
MOL718,ESTANTERÍA 1,1,1,JARRA ESTRAPREMIER 2 LITROS BASE MEZCLADOR			
MOL14087,ESTANTERÍA 1,1,2,TAPA RECIPIENTE RECTANGULAR DESPENSA 3L BAJO			
MOL4286,ESTANTERÍA 1,2,3,BEBEDERO CUERPO BRIDA			
15434,ESTANTERÍA 1,4,2,N/A
MOL4331,ESTANTERÍA 1,2,2,TAPA ESTRAPACK REDONDO # 1 - 0.25 L			
MOL15299,ESTANTERÍA 1,2,1,TAPA 6L			
MOL4287,ESTANTERÍA 1,3,1,BEBEDERO BASE INTERMEDIA BRIDA			
MOL4342,ESTANTERÍA 1,2,3,CUERPO ESTRAPACK REDONDO # 2 - 0.5 L			
MOL14191,ESTANTERÍA 1,2,2,PIN BISAGRA LOCKER			
MOL14756,H75-H76,1,2,TAPA ESTRAPACK 4			
MOL14088,ESTANTERÍA 1,2,2,RECIPIENTE CUADRADO NEVERA 0.5L			
MOL13872,ESTANTERÍA 1,2,2,TAPA OCA CUADRADO 0.25 LITROS			
MOL15204,ESTANTERÍA 1,1,2,SUJETADOR DE BOLSA 10L			
MOL892,ESTANTERÍA 1,5,2,TENSOR PARA BEBEDERO			
MOL4333,Sopladora 2,1,1,ESTIBA 26
MOL14345,Sopladora 2,1,2,ESTIBA 26
MOL13472,Sopladora 2,1,3,ESTIBA 26
MOL6886,Sopladora 2,2,1,ESTIBA 26
MOL8082,Sopladora 2,2,2,ESTIBA 26
MOL13730,Sopladora 2,2,3,ESTIBA 26  
MOL8723,ESTANTERÍA 1,1,3,PEDAL PAPELERA DE PEDAL 10 L		
MOL15265,ESTANTERÍA 1,3,3,Ventanas-Capiteles y Asta			
MOL6340,ESTANTERÍA 1,5,1,BEBDERO BASE SUPERIOR BRIDA			
MOL8581,ESTANTERÍA 1,5,1,BANDEJA CON DIVISIONES PARA RESTAURANTE			
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
            
         # --- NUEVA LÓGICA INTELIGENTE: ESTANTERÍA VS ESTIBAS/MÁQUINAS ---
            # Convertimos a mayúsculas para buscar fácilmente
            notas_texto = str(res['NOTAS']).upper()
            ubicacion_texto = str(res['UBICACIÓN']).upper()
            
            # Buscamos "ESTANTER" (sin tilde para evitar errores de tipeo)
            if "ESTANTER" in notas_texto or "ESTANTER" in ubicacion_texto:
                label_y = "NIVEL"
                label_x = "PISO"
            else:
                label_y = "FILA"
                label_x = "PUESTO"
            # ----------------------------------------------------------------
            
            # Usamos columnas laterales vacías para centrar el resultado profesionalmente
            r_left, r_mid, r_right = st.columns([1, 4, 1])
            
            with r_mid:
                # Crear una tarjeta visual profesional para el resultado
                with st.container():
                    st.success(f"📍 UBICACIÓN EN PLANTA ENCONTRADA PARA EL MOLDE: {codigo_limpio_input}")
                    
                    # Organizamos la información en métricas profesionales
                    col_met1, col_met2, col_met3 = st.columns(3)
                    with col_met1:
                        st.metric(label="UBICACIÓN / SECTOR", value=res['UBICACIÓN'])
                    with col_met2:
                        # Usamos la etiqueta dinámica calculada arriba
                        st.metric(label=label_y, value=res['FILA'])
                    with col_met3:
                        # Usamos la etiqueta dinámica calculada arriba
                        st.metric(label=label_x, value=res['PUESTO'])
                    
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
                            font-size: 20px; 
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

import streamlit as st
import openai
import os
from dotenv import load_dotenv
from PIL import Image

# Cargar las variables de entorno desde .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configuración de la página
st.set_page_config(page_title="AnuncioProAI", page_icon="🏡", layout="centered")

# Título en una sola línea
col1, col2 = st.columns([1, 5])  # Crear dos columnas
with col1:
    st.image("yo.jpg", width=500)  # Ajusta la ruta y el tamaño de la imagen
with col2:
    st.markdown("<h1 style='text-align: center;'>🏡 AnuncioProAI: Creador de anuncios inmobiliarios</h1>", unsafe_allow_html=True)

# Sección de datos del inmueble
st.subheader("📋 Características del inmueble")
tipo = st.selectbox("Tipo de propiedad", [
    "Piso", "Ático", "Dúplex", "Estudio / loft", "Casa", "Chalet", "Adosado", 
    "Bungalow", "Piso de protección oficial (VPO)", "Finca/Rural","Cortijo", "Local comercial", 
    "Oficina", "Nave industrial", "Terreno", "Mansión"
])
estado = st.selectbox("Estado", ["A demoler","A reformar", "Buen estado", "Como nuevo", "Nuevo"])
m2 = st.number_input("m² construidos", min_value=10, max_value=30000)
m2_utiles = st.number_input("m² útiles", min_value=10, max_value=30000)
m2_terreno = st.number_input("m² de terreno", min_value=0, max_value=30000)
habitaciones = st.number_input("Número de habitaciones", min_value=0, max_value=50)
baños = st.number_input("Número de baños", min_value=0, max_value=10)
fachada = st.radio("Fachada", ["Exterior", "Interior"])
ascensor = st.radio("¿Tiene ascensor?", ["Sí tiene", "No tiene"])
certificado = st.selectbox("Calificación energética", ["A", "B", "C", "D", "E", "F", "G"])
orientacion = st.selectbox("Orientación", [
    "Norte", "Sur", "Este", "Oeste", 
    "Noreste", "Noroeste", 
    "Sureste", "Suroeste"
])

# Validaciones básicas
if m2 <= 0 or m2_utiles <= 0:
    st.error("La superficie construida y útil deben ser mayores a 0.")
    st.stop()

# Selección de tipos de suelo
st.subheader("🪵 Tipos de suelo")
suelo_interior = st.selectbox("Tipo de suelo en el interior", [
    "Parquet", "Tarima flotante", "Baldosa cerámica", "Mármol", "Granito", "Vinílico", "Moqueta", "Cemento pulido", "Laminado", "Corcho"
])
suelo_exterior = st.selectbox("Tipo de suelo en el exterior", [
    "Ninguno","Grava", "Pavimento de adoquín", "Hormigón", "Terracota", "Decking de madera", "Piedra natural", "Césped artificial", "Pavimento permeable"
])

# Características adicionales
st.subheader("✨ Extras")
extras_vivienda = st.multiselect("Características de la vivienda", [
    "Amueblado", "Armarios empotrados", "Aire acondicionado", "Terraza", "Balcón", "Trastero", "Plaza de garaje"])
extras_edificio = st.multiselect("Características del edificio", ["Piscina", "Zona verde"])

# Solicitar metros cuadrados si se seleccionan terraza, balcón, trastero o plaza de garaje
metros_terraza = 0
metros_balcon = 0
metros_trastero = 0
metros_garaje = 0

if "Terraza" in extras_vivienda:
    metros_terraza = st.number_input("Metros cuadrados de la terraza", min_value=1, max_value=1000)
if "Balcón" in extras_vivienda:
    metros_balcon = st.number_input("Metros cuadrados del balcón", min_value=1, max_value=1000)
if "Trastero" in extras_vivienda:
    metros_trastero = st.number_input("Metros cuadrados del trastero", min_value=1, max_value=1000)
if "Plaza de garaje" in extras_vivienda:
    metros_garaje = st.number_input("Metros cuadrados de la plaza de garaje", min_value=1, max_value=1000)

# Localización del inmueble y descripción de los servicios cercanos
st.subheader("📍 Localización y servicios cercanos")
ubicacion = st.text_input("📍 Dirección del inmueble", "Introduce la dirección del inmueble aquí")

# Inputs para los servicios cercanos
servicios_cercanos = st.multiselect(
    "Selecciona los servicios cercanos", 
    ["Centro médico", "Colegios", "Centros comerciales", "Transporte público", "Parques", "Tiendas y restaurantes", "Gimnasios", "Farmacias", "Estaciones de tren", "Aeropuerto"]
)

# Selección si está cerca de la playa o montaña
cerca_playa = st.checkbox("Cerca de la playa")
cerca_montana = st.checkbox("Cerca de la montaña")

# Distancia a la playa o montaña (solo si se ha seleccionado una de las dos opciones)
distancia_playa = None
distancia_montana = None
if cerca_playa:
    distancia_playa = st.number_input("¿A qué distancia está la playa (en metros)?", min_value=0, step=10)
if cerca_montana:
    distancia_montana = st.number_input("¿A qué distancia está la montaña (en metros)?", min_value=0, step=10)

# Descripción de los servicios cercanos
descripcion_servicios = "Estos son los servicios cercanos a la propiedad: "
if servicios_cercanos:
    descripcion_servicios += ", ".join(servicios_cercanos)
else:
    descripcion_servicios = "No se han seleccionado servicios cercanos."

# Descripción de la cercanía a la playa o montaña
descripcion_cercania = ""
if cerca_playa:
    descripcion_cercania = f"Está a {distancia_playa} metros de la playa."
elif cerca_montana:
    descripcion_cercania = f"Está a {distancia_montana} metros de la montaña."

# Mostrar la información recopilada
st.write(f"🔑 **Dirección**: {ubicacion}")
st.write(f"🏙 **Servicios cercanos**: {descripcion_servicios}")
if descripcion_cercania:
    st.write(f"🌊/🏞 **Cercanía**: {descripcion_cercania}")

# **Nuevo**: Cargar imágenes o planos
st.subheader("📸 Añadir imágenes o planos del inmueble")
uploaded_files = st.file_uploader("Sube fotos o planos", type=["jpg", "jpeg", "png", "pdf"], accept_multiple_files=True)

# Si se suben archivos, mostrar las imágenes
if uploaded_files:
    st.write("Archivos subidos:")
    for uploaded_file in uploaded_files:
        if uploaded_file.type in ["image/jpeg", "image/png"]:
            image = Image.open(uploaded_file)
            st.image(image, caption=uploaded_file.name, use_column_width=True)
        else:
            st.write(f"Archivo {uploaded_file.name} cargado correctamente.")

# Añadir una sección para que el usuario seleccione el destino del anuncio
st.subheader("📣 Selecciona el destino del anuncio")
destino = st.radio(
    "¿Dónde quieres publicar el anuncio?",
    ("Portales inmobiliarios (Idealista, Fotocasa, Milanuncios)", "Redes sociales (Facebook, Instagram)")
)

# Botón para generar el anuncio
if st.button("📝 Generar anuncio"):
    with st.spinner("Generando anuncio..."):
        try:
            # Preparar mensaje para la IA según el destino
            if destino == "Portales inmobiliarios (Idealista, Fotocasa, Milanuncios)":
                mensaje_usuario = f"""
Redacta un anuncio inmobiliario profesional, emocional y altamente persuasivo para publicar en Idealista, Fotocasa, Milanuncios y otros portales inmobiliarios.

Datos del inmueble:
- Tipo de propiedad: {tipo}
- Estado: {estado}
- Superficie: {m2} m²
- Habitaciones: {habitaciones}
- Baños: {baños}
- Fachada: {fachada}
- Ascensor: {ascensor}
- Certificación energética: {certificado}
- Orientación: {orientacion}
- Precio: {precio} €
- Gastos de comunidad: {gastos} €/mes
- Situación legal: {situacion}

Extras:
- Piscina: {"Sí" if "Piscina" in extras_edificio else "No"}
- Terraza: {"Sí" if "Terraza" in extras_vivienda else "No"}
- Patio: {"No"}  # Default value as no input is provided for patio
- Cercanía al mar: {"No"}  # Default value as no input is provided for proximity to the sea
- Zonas comerciales cercanas: {"No"}  # Default value as no input is provided for commercial zones
- Colegios cercanos: {"No"}  # Default value as no input is provided for nearby schools
- Tiendas y restaurantes cercanos: {"No"}  # Default value as no input is provided for nearby shops/restaurants

Por favor, destaca todos estos aspectos, especialmente la piscina, la terraza, la cercanía al mar y las zonas comerciales cercanas. Crea un anuncio largo, detallado y persuasivo, resalta los beneficios emocionales de vivir en esta propiedad (luz, vistas, tranquilidad, ubicación) y termina con una llamada a la acción clara, enfocada en atraer al comprador ideal para esta propiedad.
"""

            elif destino == "Redes sociales (Facebook, Instagram)":
                mensaje_usuario = f"""
Redacta un anuncio inmobiliario atractivo y persuasivo, adecuado para publicar en redes sociales como Facebook e Instagram. El anuncio debe ser corto, visualmente impactante y emocionalmente atractivo.

Datos del inmueble:
- Tipo de propiedad: {tipo}
- Estado: {estado}
- Superficie: {m2} m²
- Habitaciones: {habitaciones}
- Baños: {baños}
- Precio: {precio} €
- Extras destacados: {', '.join(extras_vivienda) if extras_vivienda else 'Ninguno'}

Extras clave a destacar para este anuncio:
- Piscina: {"Sí" if "Piscina" in extras_edificio else "No"}
- Terraza: {"Sí" if "Terraza" in extras_vivienda else "No"}
- Cercanía al mar: {"No"}  # Default value as no input is provided for proximity to the sea
- Zonas comerciales cercanas: {"No"}  # Default value as no input is provided for commercial zones

Crea un anuncio breve, directo y emocional, destacando las características más atractivas de la propiedad, como la piscina, la terraza y la cercanía al mar. Usa frases cortas, imágenes visuales y una llamada a la acción clara, invitando a los usuarios a visitar la propiedad.
"""

            # Llamada a OpenAI usando el endpoint adecuado (v1/chat/completions)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # O el modelo que tengas disponible
                messages=[ 
                    {
                        "role": "system",
                        "content": (
                            "Eres el mayor experto en anuncios inmobiliarios, especializado en marketing emocional y persuasivo. "
                            "Debes crear anuncios que resalten los aspectos más atractivos de las propiedades, como piscina, terraza, cercanía al mar, "
                            "zonas comerciales cercanas, y la calidad de vida en la zona. Utiliza un tono atractivo y emocionante para captar la atención de los compradores, que no sean demasiado largos, pero que sean informativos y persuasivos. "
                            "Recuerda que el objetivo es atraer al comprador ideal para esta propiedad."
                        )
                    },
                    {
                        "role": "user",
                        "content": mensaje_usuario
                    }
                ]
            )

            anuncio = response['choices'][0]['message']['content']
            st.success("✅ Anuncio generado con éxito")
            st.text_area("✍️ Anuncio generado:", value=anuncio, height=300)
        
        except Exception as e:
            st.error(f"❌ Ocurrió un error: {e}")   
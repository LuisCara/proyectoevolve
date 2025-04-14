import streamlit as st
import openai
import os
from dotenv import load_dotenv
from PIL import Image
import ssl 
import certifi

# Fuerza a usar certificados válidos
os.environ['SSL_CERT_FILE'] = certifi.where()

# Cargar las variables de entorno desde .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configuración de la página
st.set_page_config(page_title="AnuncioProAI", page_icon="🏡", layout="centered")

# Título en una sola línea
col1, col2 = st.columns([1, 5])
with col1:
    st.image("yo.jpg", width=500)
with col2:
    st.markdown("<h1 style='text-align: center;'>🏡 AnuncioProAI: Creador de anuncios inmobiliarios</h1>", unsafe_allow_html=True)

# Sección de datos del inmueble
st.subheader("📋 Características del inmueble")
tipo = st.selectbox("Tipo de propiedad", [
    "Piso", "Ático", "Dúplex", "Estudio / loft", "Casa", "Chalet", "Adosado",
    "Bungalow", "Piso de protección oficial (VPO)", "Finca/Rural", "Cortijo", "Local comercial",
    "Oficina", "Nave industrial", "Terreno", "Mansión"
])
estado = st.selectbox("Estado", ["A demoler", "A reformar", "Buen estado", "Como nuevo", "Nuevo"])
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

# Selección de tipos de suelo
st.subheader("🪵 Tipos de suelo")
suelo_interior = st.selectbox("Tipo de suelo en el interior", [
    "Parquet", "Tarima flotante", "Baldosa cerámica", "Mármol", "Granito", "Vinílico", "Moqueta", "Cemento pulido", "Laminado", "Corcho"
])
suelo_exterior = st.selectbox("Tipo de suelo en el exterior", [
    "Ninguno", "Grava", "Pavimento de adoquín", "Hormigón", "Terracota", "Decking de madera", "Piedra natural", "Césped artificial", "Pavimento permeable"
])

# Características adicionales
st.subheader("✨ Extras")
extras_vivienda = st.multiselect("Características de la vivienda", [
    "Amueblado", "Armarios empotrados", "Aire acondicionado", "Terraza", "Balcón", "Trastero", "Plaza de garaje"])
extras_edificio = st.multiselect("Características del edificio", ["Piscina", "Zona verde"])

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

# Localización del inmueble y servicios cercanos
st.subheader("📍 Localización y servicios cercanos")
ubicacion = st.text_input("📍 Dirección del inmueble", "Introduce la dirección del inmueble aquí")

servicios_cercanos = st.multiselect(
    "Selecciona los servicios cercanos",
    ["Centro médico", "Colegios", "Centros comerciales", "Transporte público", "Parques", "Tiendas y restaurantes", "Gimnasios", "Farmacias", "Estaciones de tren", "Aeropuerto"]
)

cerca_playa = st.checkbox("Cerca de la playa")
cerca_montana = st.checkbox("Cerca de la montaña")

distancia_playa = None
distancia_montana = None
if cerca_playa:
    distancia_playa = st.number_input("¿A qué distancia está la playa (en metros)?", min_value=0, step=10)
if cerca_montana:
    distancia_montana = st.number_input("¿A qué distancia está la montaña (en metros)?", min_value=0, step=10)

descripcion_servicios = "Estos son los servicios cercanos a la propiedad: "
if servicios_cercanos:
    descripcion_servicios += ", ".join(servicios_cercanos)
else:
    descripcion_servicios = "No se han seleccionado servicios cercanos."

descripcion_cercania = ""
if cerca_playa:
    descripcion_cercania = f"Está a {distancia_playa} metros de la playa."
elif cerca_montana:
    descripcion_cercania = f"Está a {distancia_montana} metros de la montaña."

st.write(f"🔑 **Dirección**: {ubicacion}")
st.write(f"🏙 **Servicios cercanos**: {descripcion_servicios}")
if descripcion_cercania:
    st.write(f"🌊/🏞 **Cercanía**: {descripcion_cercania}")

# Precio y situación legal
st.subheader("💶 Precio y situación")
precio = st.number_input("Precio del inmueble (€)", min_value=0)
gastos = st.number_input("Gastos de comunidad (€ / mes)", min_value=0)
situacion = st.selectbox("¿Situación excepcional?", [
    "No, en ninguna situación excepcional", "Ocupada ilegalmente", "Alquilada, con inquilinos", "Nuda propiedad"])

# Información adicional
st.subheader("📝 Información adicional")
informacion_adicional = st.text_area("¿Hay algo más que quieras añadir sobre la propiedad?")
if informacion_adicional:
    st.write("Información adicional:", informacion_adicional)

# Imágenes o planos
st.subheader("📸 Añadir imágenes o planos del inmueble")
uploaded_files = st.file_uploader("Sube fotos o planos", type=["jpg", "jpeg", "png", "pdf"], accept_multiple_files=True)

if uploaded_files:
    st.write("Archivos subidos:")
    for uploaded_file in uploaded_files:
        if uploaded_file.type in ["image/jpeg", "image/png"]:
            image = Image.open(uploaded_file)
            st.image(image, caption=uploaded_file.name, use_container_width=True)
        else:
            st.write(f"Archivo {uploaded_file.name} cargado correctamente.")

# Destino del anuncio
st.subheader("📣 Selecciona el destino del anuncio")
destino = st.radio(
    "¿Dónde quieres publicar el anuncio?",
    ("Portales inmobiliarios (Idealista, Fotocasa, Milanuncios)", "Redes sociales (Facebook, Instagram)")
)

# Función para recopilar datos
def recopilar_datos():
    return {
        "tipo": tipo,
        "estado": estado,
        "m2": m2,
        "m2_utiles": m2_utiles,
        "m2_terreno": m2_terreno,
        "habitaciones": habitaciones,
        "baños": baños,
        "fachada": fachada,
        "ascensor": ascensor,
        "certificado": certificado,
        "orientacion": orientacion,
        "suelo_interior": suelo_interior,
        "suelo_exterior": suelo_exterior,
        "extras_vivienda": extras_vivienda,
        "extras_edificio": extras_edificio,
        "metros_terraza": metros_terraza,
        "metros_balcon": metros_balcon,
        "metros_trastero": metros_trastero,
        "metros_garaje": metros_garaje,
        "ubicacion": ubicacion,
        "servicios_cercanos": servicios_cercanos,
        "descripcion_servicios": descripcion_servicios,
        "descripcion_cercania": descripcion_cercania,
        "precio": precio,
        "gastos": gastos,
        "situacion": situacion,
        "informacion_adicional": informacion_adicional,
        "destino": destino
    }

# Función para generar el anuncio con la nueva API de OpenAI
def generar_anuncio(datos):
    prompt = f"""
Eres un experto copywriter especializado en redactar anuncios inmobiliarios persuasivos y profesionales. 
Crea un anuncio de alto nivel para una propiedad con las siguientes características:

🏡 Tipo de propiedad: {datos['tipo']}
📍 Ubicación: {datos['ubicacion']}
📐 Superficie: {datos['m2']} m² construidos, {datos['m2_utiles']} m² útiles, {datos['m2_terreno']} m² de terreno
🛏 Habitaciones: {datos['habitaciones']}, 🛁 Baños: {datos['baños']}
🌞 Fachada: {datos['fachada']} | Orientación: {datos['orientacion']}
📈 Estado: {datos['estado']}, Certificado energético: {datos['certificado']}
🏗 Suelo interior: {datos['suelo_interior']}, exterior: {datos['suelo_exterior']}
✨ Extras vivienda: {', '.join(datos['extras_vivienda']) if datos['extras_vivienda'] else 'Ninguno'}
🏢 Extras edificio: {', '.join(datos['extras_edificio']) if datos['extras_edificio'] else 'Ninguno'}
📸 Terraza: {datos['metros_terraza']} m², Balcón: {datos['metros_balcon']} m², Trastero: {datos['metros_trastero']} m², Garaje: {datos['metros_garaje']} m²
🗺 Servicios cercanos: {datos['descripcion_servicios']}
🌊/🏞 Otros: {datos['descripcion_cercania']}
💶 Precio: {datos['precio']} € | Gastos comunidad: {datos['gastos']} €
⚠ Situación: {datos['situacion']}
📝 Información adicional: {datos['informacion_adicional']}
📣 Destino del anuncio: {datos['destino']}

El texto debe ser atractivo, persuasivo, sin repetir datos de forma robótica. Usa frases emotivas, beneficios para el comprador y estilo comercial. Añade emojis si es para redes sociales.
"""

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1000
    )

    return response.choices[0].message.content

# Botón para generar el anuncio
st.subheader("🧠 Generador de anuncio con IA")
if st.button("✨ Generar anuncio optimizado"):
    datos = recopilar_datos()
    anuncio = generar_anuncio(datos)
    st.success("✅ Anuncio generado con éxito:")
    st.text_area("📝 Anuncio generado", value=anuncio, height=300)

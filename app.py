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

# Selección de tipos de suelo
st.subheader("🪵 Tipos de suelo")
suelo_interior = st.selectbox("Tipo de suelo en el interior", [
    "Parquet", "Tarima flotante", "Baldosa cerámica", "Mármol", "Granito", "Vinílico", "Moqueta", "Cemento pulido", "Laminado", "Corcho"
])
suelo_exterior = st.selectbox("Tipo de suelo en el exterior", [
    "Grava", "Pavimento de adoquín", "Hormigón", "Terracota", "Decking de madera", "Piedra natural", "Césped artificial", "Pavimento permeable"
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

# Precio y situación legal
st.subheader("💶 Precio y situación")
precio = st.number_input("Precio del inmueble (€)", min_value=0)
gastos = st.number_input("Gastos de comunidad (€ / mes)", min_value=0)
situacion = st.selectbox("¿Situación excepcional?", [
    "No, en ninguna situación excepcional", "Ocupada ilegalmente", "Alquilada, con inquilinos", "Nuda propiedad"])

# preguntar al usuario si quiere añadir alguna informacion adicional de la propiedad que sea relevante
st.subheader("📝 Información adicional")
informacion_adicional = st.text_area("¿Hay algo más que quieras añadir sobre la propiedad?")
if informacion_adicional:
    st.write("Información adicional:", informacion_adicional)

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
- Extras de la vivienda: {', '.join(extras_vivienda) if extras_vivienda else 'Ninguno'}
- Extras del edificio: {', '.join(extras_edificio) if extras_edificio else 'Ninguno'}
- Precio: {precio} €
- Gastos de comunidad: {gastos} €/mes
- Situación legal: {situacion}

Crea un anuncio largo, detallado y persuasivo, resalta los beneficios de vivir en esta propiedad, incluye detalles que evoquen emociones positivas (luz, vistas, tranquilidad, ubicación, etc.) y termina con una llamada a la acción clara. Hazlo atractivo para los posibles compradores en portales inmobiliarios.
"""

            elif destino == "Redes sociales (Facebook, Instagram)":
                mensaje_usuario = f"""
Redacta un anuncio inmobiliario atractivo y persuasivo, adecuado para publicar en redes sociales como Facebook e Instagram. El anuncio debe ser corto y visualmente impactante.

Datos del inmueble:
- Tipo de propiedad: {tipo}
- Estado: {estado}
- Superficie: {m2} m²
- Habitaciones: {habitaciones}
- Baños: {baños}
- Precio: {precio} €
- Extras destacados: {', '.join(extras_vivienda) if extras_vivienda else 'Ninguno'}

Crea un anuncio breve, directo y emocional, destacando las características más atractivas de la propiedad. Utiliza frases cortas, imágenes visuales y una llamada a la acción clara. El anuncio debe ser conciso para captar la atención de los usuarios de redes sociales y generar interacción.
"""

            # Llamada a OpenAI usando el endpoint adecuado (v1/chat/completions)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # O el modelo que tengas disponible
                messages=[ 
                    {
                        "role": "system",
                        "content": (
                            "Eres el mejor redactor de anuncios inmobiliarios, experto en marketing emocional, técnicas de venta persuasiva "
                            "y copywriting. Crea textos que enamoren y vendan propiedades en segundos."
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
            st.error(f"❌ Error al generar el anuncio: {e}")

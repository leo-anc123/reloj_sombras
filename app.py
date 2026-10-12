import streamlit as st
import time
import random
import os
import base64
from gtts import gTTS

st.set_page_config(page_title="Reloj de Sombras TT", page_icon="🏓", layout="centered")

@st.cache_data
def preparar_audios():
    golpes = {
        # Audios optimizados (cortos)
        "drive": "Drive", 
        "reves": "Revés",
        # Audios explícitos (solo para modo mixto)
        "top_drive": "Top Drive",
        "top_reves": "Top Revés",
        "corto_drive": "Corto Drive",
        "corto_reves": "Corto Revés",
        # Audio de preparación
        "countdown": "Inicio de entrenamiento en 3... 2... 1..."
    }
    
    if not os.path.exists("audios"):
        os.makedirs("audios")
        
    for clave, texto in golpes.items():
        archivo = f"audios/{clave}.mp3"
        if not os.path.exists(archivo):
            tts = gTTS(text=texto, lang='es', tld='com.ar')
            tts.save(archivo)
            
preparar_audios()

def reproducir_audio(clave):
    """Inyecta el reproductor HTML5 oculto para que suene en el celular."""
    archivo = f"audios/{clave}.mp3"
    with open(archivo, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        audio_html = f"""
            <audio autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.empty().markdown(audio_html, unsafe_allow_html=True)

# --- Interfaz de Usuario ---
st.title("🏓 Reloj de Sombras v2.0")

st.sidebar.header("⚙️ Configuración")
series = st.sidebar.number_input("Cantidad de Series", 1, 10, 3)
golpes_por_serie = st.sidebar.number_input("Golpes por Serie", 5, 50, 20)
tiempo_base = st.sidebar.slider("Tiempo Base (segundos)", 1.0, 4.0, (1.5, 3.0))

categoria = st.sidebar.selectbox(
    "Categoría de Trabajo",
    ["Básico", "Topspin", "Corto", "Mixto (Todo)"]
)

# --- Lógica de Contexto ---
# Cada opción es una tupla: (archivo_de_audio_a_reproducir, texto_a_mostrar_en_pantalla)
if categoria == "Básico":
    opciones = [("drive", "DRIVE"), ("reves", "REVÉS")]
elif categoria == "Topspin":
    # Audio corto, pero pantalla indica la variante técnica
    opciones = [("drive", "TOPSPIN DRIVE"), ("reves", "TOPSPIN REVÉS")]
elif categoria == "Corto":
    # Audio corto, pero pantalla indica la variante técnica
    opciones = [("drive", "CORTO DRIVE"), ("reves", "CORTO REVÉS")]
else:
    # Modo Mixto: Audio explícito completo y texto completo
    opciones = [
        ("drive", "DRIVE"), 
        ("reves", "REVÉS"),
        ("top_drive", "TOP DRIVE"),
        ("top_reves", "TOP REVÉS"),
        ("corto_drive", "CORTO DRIVE"),
        ("corto_reves", "CORTO REVÉS")
    ]

# --- Ejecución ---
if st.button("🔴 COMENZAR RUTINA", use_container_width=True):
    zona_mensaje = st.empty()
    zona_golpe = st.empty()
    
    for serie in range(1, series + 1):
        ajuste = (serie - 1) * 0.2
        t_min = max(0.5, tiempo_base[0] - ajuste)
        t_max = max(1.0, tiempo_base[1] - ajuste)
        
        zona_mensaje.info(f"Serie {serie}/{series} - En posición...")
        
        # 1. Ejecutar la cuenta regresiva al inicio de la serie
        reproducir_audio("countdown")
        zona_golpe.warning("Iniciando en 3... 2... 1...")
        time.sleep(4.5) # Espera a que termine la locución
        
        for golpe_num in range(1, golpes_por_serie + 1):
            espera = random.uniform(t_min, t_max)
            zona_golpe.subheader("⏳ (Split-step listos)...")
            
            time.sleep(espera)
            
            # 2. Desempaquetar la tupla de audio y texto visual
            clave_audio, texto_pantalla = random.choice(opciones)
            
            zona_golpe.error(f"¡{texto_pantalla}!")
            reproducir_audio(clave_audio)
            
            time.sleep(0.8) # Pausa mínima para no superponer audios
            
        if serie < series:
            zona_mensaje.success(f"✅ Serie {serie} terminada. Descanso de 10 segundos.")
            zona_golpe.empty()
            time.sleep(10)
            
    zona_mensaje.success("🎉 ¡Entrenamiento finalizado! Buen trabajo de piernas.")
    zona_golpe.empty()
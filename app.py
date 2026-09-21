import streamlit as st
import time
import random
import os
import base64
from gtts import gTTS

# Configuración inicial de la página
st.set_page_config(page_title="Reloj de Sombras TT", page_icon="🏓", layout="centered")

# --- Preparación de Audio (Caché para no descargar múltiples veces) ---
@st.cache_data
def preparar_audios():
    golpes = {
        "drive": "Drive", 
        "reves": "Revés",
        "top_drive": "Top de drive",
        "top_reves": "Top de revés",
        "corto_drive": "Corto de drive",
        "corto_reves": "Corto de revés"
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
        # st.empty() permite sobreescribir el componente para no llenar la pantalla de reproductores
        st.empty().markdown(audio_html, unsafe_allow_html=True)

# --- Interfaz de Usuario ---
st.title("🏓 Reloj de Sombras")
st.write("Entrenamiento de reacción y split-step.")

st.sidebar.header("⚙️ Configuración")
series = st.sidebar.number_input("Cantidad de Series", 1, 10, 3)
golpes_por_serie = st.sidebar.number_input("Golpes por Serie", 5, 50, 20)
tiempo_base = st.sidebar.slider("Tiempo Base (segundos)", 1.0, 4.0, (1.5, 3.0))

categoria = st.sidebar.selectbox(
    "Categoría de Trabajo",
    ["Ataque (Tops y bloqueos)", "Corto", "Básico", "Mixto (Todo)"]
)

# Definir los arrays de golpes según la selección
if categoria == "Básico":
    opciones = ["drive", "reves"]
elif categoria == "Ataque (Tops y bloqueos)":
    opciones = ["top_drive", "top_reves", "drive", "reves"]
elif categoria == "Corto":
    opciones = ["corto_drive", "corto_reves"]
else:
    opciones = ["drive", "reves", "top_drive", "top_reves", "corto_drive", "corto_reves"]

# --- Lógica de Ejecución ---
if st.button("🔴 COMENZAR RUTINA", use_container_width=True):
    zona_mensaje = st.empty()
    zona_golpe = st.empty()
    
    for serie in range(1, series + 1):
        # Dificultad progresiva: reducimos 0.2s el intervalo por cada serie
        ajuste = (serie - 1) * 0.2
        t_min = max(0.5, tiempo_base[0] - ajuste)
        t_max = max(1.0, tiempo_base[1] - ajuste)
        
        zona_mensaje.info(f"Serie {serie}/{series} - Prepárate...")
        time.sleep(3) 
        
        for golpe_num in range(1, golpes_por_serie + 1):
            espera = random.uniform(t_min, t_max)
            zona_golpe.subheader("⏳ Esperando señal (Split-step listos)...")
            
            time.sleep(espera)
            
            golpe_actual = random.choice(opciones)
            
            # Mostrar visualmente el golpe en grande
            zona_golpe.error(f"¡{golpe_actual.replace('_', ' ').upper()}!")
            
            # Activar el sonido
            reproducir_audio(golpe_actual)
            
            time.sleep(0.8) # Pausa mínima para que el audio termine antes del próximo ciclo
            
        if serie < series:
            zona_mensaje.success(f"✅ Serie {serie} terminada. Descanso de 10 segundos.")
            zona_golpe.empty()
            time.sleep(10)
            
    zona_mensaje.success("🎉 ¡Entrenamiento finalizado! Buen trabajo de piernas.")
    zona_golpe.empty()
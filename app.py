import streamlit as st
import time
import random
import os
import base64
from gtts import gTTS

st.set_page_config(page_title="Reloj de Sombras TT", page_icon="🏓", layout="wide")

# --- 1. Preparación de Audios en Memoria (Diccionario Base64) ---
@st.cache_data
def cargar_audios_b64():
    """Genera los mp3 (incluyendo Flicks) y devuelve un diccionario en Base64."""
    golpes = {
        "drive": "Drive", 
        "reves": "Revés",
        "top_drive": "Top Drive",
        "top_reves": "Top Revés",
        "corto_drive": "Corto Drive",
        "corto_reves": "Corto Revés",
        "flick_drive": "Flick Drive",
        "flick_reves": "Flick Revés",
        "pivot": "Pivot",
        "freno": "Quietos",
        "intro": "Inicio de entrenamiento",
        "3": "Tres",
        "2": "Dos",
        "1": "Uno"
    }
    
    if not os.path.exists("audios"):
        os.makedirs("audios")
        
    audios_codificados = {}
    for clave, texto in golpes.items():
        archivo = f"audios/{clave}_v2.mp3" if "flick" in clave else f"audios/{clave}.mp3"
        if not os.path.exists(archivo):
            tts = gTTS(text=texto, lang='es', tld='com.ar')
            tts.save(archivo)
        with open(archivo, "rb") as f:
            audios_codificados[clave] = base64.b64encode(f.read()).decode()
            
    return audios_codificados

AUDIOS_B64 = cargar_audios_b64()

# --- 2. Motor Gráfico + Audio Unificado ---
def renderizar_tablero(color_fondo, icono, texto, subtexto="", clave_audio=None):
    """Renderiza el tablero visual e inyecta el audio directamente en el mismo bloque DOM."""
    bloque_texto = (
        f'<div style="font-size: 4rem; font-weight: 900; color: white; font-family: sans-serif; '
        f'text-transform: uppercase; letter-spacing: 2px; text-shadow: 2px 2px 8px rgba(0,0,0,0.5);">{texto}</div>'
        if texto else ""
    )
    
    bloque_audio = ""
    if clave_audio and clave_audio in AUDIOS_B64:
        b64 = AUDIOS_B64[clave_audio]
        uid = f"{clave_audio}_{time.time()}"
        bloque_audio = (
            f'<audio id="{uid}" autoplay="true" style="display:none;">'
            f'<source src="data:audio/mp3;base64,{b64}" type="audio/mp3">'
            f'</audio>'
        )
    
    html_code = (
        f'<div style="background-color: {color_fondo}; height: 65vh; display: flex; flex-direction: column; '
        f'justify-content: center; align-items: center; border-radius: 25px; box-shadow: 0 10px 25px rgba(0,0,0,0.4); '
        f'padding: 20px; text-align: center; border: 4px solid rgba(255,255,255,0.2);">'
        f'<div style="font-size: 8.5rem; line-height: 1; margin-bottom: 10px;">{icono}</div>'
        f'{bloque_texto}'
        f'<div style="font-size: 1.8rem; font-weight: 600; color: rgba(255,255,255,0.9); margin-top: 10px; font-family: sans-serif;">{subtexto}</div>'
        f'{bloque_audio}'
        f'</div>'
    )
    return html_code

# --- 3. Catálogo de Estímulos (Con Flicks en Púrpura/Violeta) ---
CATALOGO_ESTIMULOS = {
    "drive":       {"audio": "drive",       "texto": "DRIVE",       "icono": "➡️",   "color": "#E65100"}, # Naranja
    "reves":       {"audio": "reves",       "texto": "REVÉS",       "icono": "⬅️",   "color": "#BF360C"}, # Naranja oscuro
    "top_drive":   {"audio": "top_drive",   "texto": "TOP DRIVE",   "icono": "↗️",   "color": "#D32F2F"}, # Rojo intenso
    "top_reves":   {"audio": "top_reves",   "texto": "TOP REVÉS",   "icono": "↖️",   "color": "#B71C1C"}, # Rojo sangre
    "corto_drive": {"audio": "corto_drive", "texto": "CORTO DRIVE", "icono": "↘️",   "color": "#1976D2"}, # Azul
    "corto_reves": {"audio": "corto_reves", "texto": "CORTO REVÉS", "icono": "↙️",   "color": "#0D47A1"}, # Azul marino
    "flick_drive": {"audio": "flick_drive", "texto": "FLICK DRIVE", "icono": "⚡↗️", "color": "#8E24AA"}, # Púrpura vibrante
    "flick_reves": {"audio": "flick_reves", "texto": "FLICK REVÉS", "icono": "⚡↖️", "color": "#4A148C"}, # Violeta profundo
    "pivot":       {"audio": "pivot",       "texto": "PIVOT DRIVE", "icono": "🔄",   "color": "#F57F17"}, # Amarillo/Oro
    "freno":       {"audio": "freno",       "texto": "¡QUIETO!",    "icono": "✋",   "color": "#2E7D32"}  # Verde
}

# --- 4. Barra Lateral de Configuración ---
st.sidebar.header("⚙️ Configuración")

modo_estimulo = st.sidebar.radio(
    "Modo de Estímulo",
    ["👁️ Solo Visual (Silencioso)", "👁️+🔊 Híbrido (Visual + Voz)", "🔊 Solo Voz (Clásico)"]
)

# Diccionario de rutinas organizadas por foco individual y niveles mixtos
RUTINAS = {
    "🎯 Foco: Básico (Drive y Revés)": {
        "claves": ["drive", "reves"],
        "audio_corto": True
    },
    "🎯 Foco: Cortos (Push)": {
        "claves": ["corto_drive", "corto_reves"],
        "audio_corto": True
    },
    "🎯 Foco: Flicks (Ataque en mesa)": {
        "claves": ["flick_drive", "flick_reves"],
        "audio_corto": True
    },
    "🎯 Foco: Topspin": {
        "claves": ["top_drive", "top_reves"],
        "audio_corto": True
    },
    "🔥 Mixto Nivel 1: Cortos + Básicos": {
        "claves": ["corto_drive", "corto_reves", "drive", "reves"],
        "audio_corto": False
    },
    "🔥 Mixto Nivel 2: Cortos + Flicks (Juego en red)": {
        "claves": ["corto_drive", "corto_reves", "flick_drive", "flick_reves"],
        "audio_corto": False
    },
    "🔥 Mixto Nivel 3: Cortos + Topspin (3ra Pelota)": {
        "claves": ["corto_drive", "corto_reves", "top_drive", "top_reves"],
        "audio_corto": False
    },
    "🔥 Mixto Nivel 4: Cortos + Flicks + Básicos": {
        "claves": ["corto_drive", "corto_reves", "flick_drive", "flick_reves", "drive", "reves"],
        "audio_corto": False
    },
    "🔥 Mixto Nivel 5: Cortos + Flicks + Topspin": {
        "claves": ["corto_drive", "corto_reves", "flick_drive", "flick_reves", "top_drive", "top_reves"],
        "audio_corto": False
    },
    "👑 Mixto Nivel PRO: Todas las variantes + Pivot": {
        "claves": [
            "drive", "reves", "corto_drive", "corto_reves",
            "flick_drive", "flick_reves", "top_drive", "top_reves", "pivot"
        ],
        "audio_corto": False
    }
}

categoria = st.sidebar.selectbox("Categoría de Trabajo", list(RUTINAS.keys()))

incluir_freno = st.sidebar.checkbox("Añadir Trampa Visual (Verde = No moverse)", value=True)
ocultar_texto = st.sidebar.checkbox("Modo Pro: Ocultar texto (Solo flechas y color)", value=False)

series = st.sidebar.number_input("Cantidad de Series", 1, 10, 3)
golpes_por_serie = st.sidebar.number_input("Golpes por Serie", 5, 50, 20)
tiempo_base = st.sidebar.slider("Tiempo entre golpes (seg)", 0.8, 4.0, (1.5, 2.8))

# --- 5. Selección de Golpes Activos ---
claves_activas = list(RUTINAS[categoria]["claves"])
forzar_audio_corto = RUTINAS[categoria]["audio_corto"]

if incluir_freno:
    claves_activas.append("freno")

# --- 6. Interfaz Principal ---
st.title("🏓 Reloj de Sombras v3.3 — Sistema de Niveles y Flicks")

with st.expander("📖 Ver Leyenda de Colores y Flechas"):
    st.markdown("""
    * 🟥 **ROJO (`↗️` / `↖️`):** Topspin / Ataque liftado (Media distancia).
    * 🟪 **PÚRPURA (`⚡↗️` / `⚡↖️`):** Flick de Drive o Revés (Ataque explosivo de muñeca sobre la mesa).
    * 🟦 **AZUL (`↘️` / `↙️`):** Corto / Push dentro de la mesa.
    * 🟧 **NARANJA (`➡️` / `⬅️`):** Golpe plano o bloqueo básico.
    * 🟨 **AMARILLO (`🔄`):** Pivotar en esquina de revés para pegar Drive.
    * 🟩 **VERDE (`✋`):** ¡Freno! Haz el split-step pero congélate sin sacar el brazo.
    """)

zona_tablero = st.empty()

zona_tablero.markdown(
    renderizar_tablero("#1E1E2E", "🏓", "LISTO PARA ENTRENAR", f"Modalidad: {categoria}"),
    unsafe_allow_html=True
)

if st.button("🔴 COMENZAR ENTRENAMIENTO", use_container_width=True):
    
    usar_voz = modo_estimulo in ["👁️+🔊 Híbrido (Visual + Voz)", "🔊 Solo Voz (Clásico)"]
    modo_solo_voz = (modo_estimulo == "🔊 Solo Voz (Clásico)")
    
    for serie in range(1, series + 1):
        ajuste = (serie - 1) * 0.15
        t_min = max(0.6, tiempo_base[0] - ajuste)
        t_max = max(1.0, tiempo_base[1] - ajuste)
        
        # 1. Aviso de Preparación
        zona_tablero.markdown(
            renderizar_tablero("#37474F", "🏓", "EN POSICIÓN...", f"Serie {serie} de {series}", clave_audio="intro"),
            unsafe_allow_html=True
        )
        time.sleep(2.2)
        
        # 2. Cuenta regresiva 3, 2, 1 sincronizada
        for seg in ["3", "2", "1"]:
            zona_tablero.markdown(
                renderizar_tablero("#263238", "⏱️", f"¡{seg}!", f"Serie {serie} de {series}", clave_audio=seg),
                unsafe_allow_html=True
            )
            time.sleep(1.0)
            
        for golpe_num in range(1, golpes_por_serie + 1):
            # Fase 1: Pantalla neutra de espera (Split-Step)
            espera = random.uniform(t_min, t_max)
            zona_tablero.markdown(
                renderizar_tablero("#121212", "⚡", "" if ocultar_texto else "SPLIT-STEP", f"Golpe {golpe_num}/{golpes_por_serie}", clave_audio=None),
                unsafe_allow_html=True
            )
            time.sleep(espera)
            
            # Fase 2: Elegir golpe y definir audio/visual
            clave_elegida = random.choice(claves_activas)
            datos_golpe = CATALOGO_ESTIMULOS[clave_elegida]
            
            # Si estamos en categoría de un solo tipo (ej. Solo Flicks), dice solo "Drive" o "Revés" para ir más rápido
            sonido_actual = None
            if usar_voz:
                if forzar_audio_corto and clave_elegida in ["top_drive", "corto_drive", "flick_drive"]:
                    sonido_actual = "drive"
                elif forzar_audio_corto and clave_elegida in ["top_reves", "corto_reves", "flick_reves"]:
                    sonido_actual = "reves"
                else:
                    sonido_actual = datos_golpe["audio"]
            
            if modo_solo_voz:
                color_mostrar = "#1E1E2E"
                icono_mostrar = "🔊"
                texto_mostrar = "" if ocultar_texto else datos_golpe["texto"]
            else:
                color_mostrar = datos_golpe["color"]
                icono_mostrar = datos_golpe["icono"]
                texto_mostrar = "" if ocultar_texto else datos_golpe["texto"]
            
            # Impacto Visual + Auditivo simultáneo
            zona_tablero.markdown(
                renderizar_tablero(
                    color_mostrar, 
                    icono_mostrar, 
                    texto_mostrar, 
                    f"Golpe {golpe_num}/{golpes_por_serie}",
                    clave_audio=sonido_actual
                ),
                unsafe_allow_html=True
            )
            
            time.sleep(1.1)
            
        if serie < series:
            for d in range(10, 0, -1):
                zona_tablero.markdown(
                    renderizar_tablero("#004D40", "🧘‍♂️", f"DESCANSO: {d}s", f"Serie {serie} completada", clave_audio=None),
                    unsafe_allow_html=True
                )
                time.sleep(1)
                
    zona_tablero.markdown(
        renderizar_tablero("#1B5E20", "🎉", "¡ENTRENAMIENTO TERMINADO!", "Excelente velocidad de reacción", clave_audio=None),
        unsafe_allow_html=True
    )
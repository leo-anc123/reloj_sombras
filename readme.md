# 🏓 Reloj de Sombras v3.0 — Entrenamiento Neuro-Motor para Tenis de Mesa

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![gTTS](https://img.shields.io/badge/Audio-gTTS%20%2B%20HTML5-success)
![Estado](https://img.shields.io/badge/Estado-En%20Producción-brightgreen)

Aplicación web interactiva diseñada para el entrenamiento individual de **reacción, desplazamientos (*footwork*) y sincronización del *split-step*** en tenis de mesa. 

El sistema simula la incertidumbre de un partido real emitiendo estímulos **auditivos, visuales o híbridos** en intervalos de tiempo aleatorios y progresivos, permitiendo entrenar sombras (*shadow play*) sin necesidad de un compañero o robot lanzapelotas.

🔗 **[Probar la Aplicación en Vivo aquí]( REEMPLAZA_CON_TU_LINK_DE_STREAMLIT )**

---

## 🎯 El Problema y la Solución

Al entrenar desplazamientos en solitario ("hacer sombras"), el jugador suele caer en un ritmo predecible y mecanizado, iniciando el movimiento desde la inmovilidad en lugar de reaccionar a una señal externa.

**Reloj de Sombras v3.0** resuelve esto mediante tres pilares del entrenamiento deportivo moderno:
1. **Activación del *Split-Step*:** Intervalos irregulares que obligan al jugador a mantener la tensión activa y saltar justo en el instante del estímulo.
2. **Estímulo Periférico y Visual:** Un tablero de alto contraste (colores y vectores direccionales) para entrenar la velocidad de procesamiento visual sin depender únicamente del oído.
3. **Inhibición Cognitiva (Freno):** Inclusión de señales "trampa" (color verde) donde el jugador debe realizar el *split-step* pero frenar el golpe en seco, simulando pelotas que tocan la red o cambios bruscos de decisión.

---

## ✨ Características Principales (v3.0)

* **3 Modos de Estímulo:**
  * 👁️ **Solo Visual (Silencioso):** Destellos de pantalla completa con código de colores y flechas direccionales.
  * 👁️+🔊 **Híbrido:** Combinación de impacto visual y comando de voz.
  * 🔊 **Solo Voz:** Entrenamiento clásico guiado por locución.
* **Modo Pro (Sin Texto):** Opción para ocultar las palabras en pantalla, forzando al cerebro a reaccionar puramente al color y a la dirección espacial en menos de 250 ms.
* **Optimización de Latencia Contextual:** En categorías específicas (ej. *Solo Topspin* o *Solo Corto*), el motor acorta la locución a *"Drive"* o *"Revés"* para minimizar el tiempo de reproducción del audio y evitar retrasos entre golpes rápidos.
* **Sobrecarga Progresiva Automática:** El intervalo de tiempo entre golpes se reduce automáticamente en `-0.15s` con cada nueva serie para simular la exigencia física y mental bajo fatiga.
* **Reproducción de Audio *Client-Side*:** Inyección dinámica de audio en Base64 mediante etiquetas HTML5 `<audio autoplay>`, permitiendo que el sonido se reproduzca directamente en el navegador del celular sin bloqueos del servidor.

---

## 🎨 Código de Colores y Estímulos

| Color | Ícono | Comando | Acción Técnica en la Mesa |
| :--- | :---: | :--- | :--- |
| 🟥 **Rojo** | `↗️` / `↖️` | **Top Drive / Revés** | Ataque ofensivo con efecto liftado (*Topspin*). |
| 🟦 **Azul** | `↘️` / `↙️` | **Corto Drive / Revés** | Paso adentro de la mesa para recepción corta (*Push/Drop*). |
| 🟧 **Naranja** | `➡️` / `⬅️` | **Drive / Revés** | Golpe plano básico o bloqueo en zona media. |
| 🟨 **Amarillo** | `🔄` | **Pivot Drive** | Desplazamiento rápido a la esquina del revés para atacar de derecha. |
| 🟩 **Verde** | `✋` | **¡Quieto! (Freno)** | *Inhibición:* Hacer el *split-step* pero congelar el brazo sin golpear. |

---

## 🛠️ Stack Tecnológico y Arquitectura

* **Lenguaje:** Python
* **Frontend / UI:** Streamlit + Inyección de HTML5 y CSS3 dinámico (`st.empty().markdown`) para renderizado de baja latencia y alto contraste.
* **Síntesis de Voz (TTS):** `gTTS` (Google Text-to-Speech) con caché persistente (`@st.cache_data`) para generar los archivos `.mp3` una única vez en el servidor y evitar llamadas repetitivas a la API durante la rutina.
* **Codificación Multimedia:** `base64` nativo para incrustar los flujos de audio directamente en el DOM del navegador móvil.

---

## 🚀 Instalación y Uso Local

Si deseas clonar este repositorio y ejecutarlo en tu propia máquina:

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/TU_USUARIO/TU_REPOSITORIO.git](https://github.com/TU_USUARIO/TU_REPOSITORIO.git)
   cd TU_REPOSITORIO
   ```

2. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación:**
   ```bash
   streamlit run app.py
   ```

---

## 📈 Roadmap (Próximas Mejoras)

- [ ] **Dashboard de Fin de Sesión:** Resumen estadístico con distribución de golpes realizados y tiempo total de trabajo neto.
- [ ] **Modo Táctico (Saque + 3ra Pelota):** Generador de secuencias de servicio y ataque posterior.
- [ ] **Visión Artificial (MediaPipe):** Control de postura en tiempo real mediante la cámara para alertar si el jugador sube demasiado su centro de gravedad (ángulo de rodillas > 150°).

---

## 👤 Autor

Desarrollado por **Leandro Ancalipe**  
*Proyecto de desarrollo en Python aplicado al rendimiento deportivo.*
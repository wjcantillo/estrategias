# 📊 Generador de Estrategias BSC con IA (Hugging Face API)

Este proyecto permite a los estudiantes generar y comparar estrategias del Balanced Scorecard (BSC) usando **Inteligencia Artificial**, sin necesidad de montar un backend propio.  
La aplicación está hecha en **Streamlit** y se conecta directamente a la **Hugging Face Inference API**.

---

## 🚀 Funcionalidades
- Subir un archivo Excel con las columnas: `Perspectiva`, `Objetivo`, `Meta`, `Indicador`, `Iniciativa`.
- Seleccionar una fila del archivo.
- Escribir una estrategia **manual**.
- Generar automáticamente una estrategia **con IA** (modelo `google/flan-t5-small`).
- Comparar ambas estrategias dentro de la misma app.

---

## 📦 Requisitos

Instala las dependencias con:

```bash
pip install -r requirements.txt
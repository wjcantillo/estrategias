import streamlit as st
import pandas as pd
import requests
import os

st.set_page_config(page_title="Comparador de Estrategias BSC", layout="centered")
st.title("Generador de Estrategias del Balanced Scorecard con Hugging Face API")

# Campo para token (los estudiantes también pueden usar uno gratuito propio)
HF_TOKEN = os.getenv("HF_TOKEN")

archivo = st.file_uploader("Sube tu archivo Excel con columnas: Perspectiva, Objetivo, Meta, Indicador, Iniciativa", type=["xlsx"])

if archivo and HF_TOKEN:
    df = pd.read_excel(archivo)
    st.dataframe(df)

    index = st.number_input("Selecciona la fila:", 0, len(df)-1)
    objetivo = df.loc[index, "Objetivo"]
    iniciativa = df.loc[index, "Iniciativa"]

    if st.button("Generar Estrategia con IA"):
        api_url = "https://api-inference.huggingface.co/models/google/flan-t5-small"
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        payload = {
            "inputs": f"Eres un experto en estrategia organizacional.\nObjetivo: {objetivo}\nIniciativa: {iniciativa}\nRedacta una estrategia clara y coherente."
        }

        try:
            response = requests.post(api_url, headers=headers, json=payload)
            if response.status_code == 200:
                output = response.json()
                estrategia_ia = output[0]["generated_text"]
                st.success("Estrategia IA generada:")
                st.write(estrategia_ia)
            else:
                st.error(f"Error en Hugging Face API: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Error de conexión con la API: {e}")
else:
    st.info("Sube el Excel y coloca un token válido de Hugging Face para continuar.")

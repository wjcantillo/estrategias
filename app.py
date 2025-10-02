import streamlit as st
import pandas as pd
from transformers import pipeline
# import requests
# import os

st.set_page_config(page_title="Comparador de Estrategias BSC", layout="centered")
st.title("Generador de Estrategias del Balanced Scorecard con Hugging Face API")

# Cargar modelo localmente (puede tardar la primera vez)
@st.cache_resource
def load_model():
    return pipeline("text2text-generation", model="google/flan-t5-small")

generator = load_model()

# Campo para token (los estudiantes también pueden usar uno gratuito propio)
# HF_TOKEN = os.getenv("HF_TOKEN")

archivo = st.file_uploader("Sube tu archivo Excel con columnas: Perspectiva, Objetivo, Meta, Indicador, Iniciativa", type=["xlsx"])

#if archivo and HF_TOKEN:
if archivo:
    df = pd.read_excel(archivo)
    st.dataframe(df)

    index = st.number_input("Selecciona la fila:", 0, len(df)-1)
    objetivo = df.loc[index, "Objetivo"]
    iniciativa = df.loc[index, "Iniciativa"]

    if st.button("Generar Estrategia con IA"):
        prompt = f"""Eres un experto en planeación estratégica. Objetivo: {objetivo} Iniciativa: {iniciativa} Redacta una estrategia clara que relacione la iniciativa con el cumplimiento del objetivo."""
        # api_url = "https://api-inference.huggingface.co/models/google/flan-t5-small"
        # headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        # payload = {
        #    "inputs": f"Eres un experto en estrategia organizacional.\nObjetivo: {objetivo}\nIniciativa: {iniciativa}\nRedacta una estrategia clara y coherente."
        # }

        try:
            result = generator(prompt, max_length=256, do_sample=True, temperature=0.7)
            estrategia_ia = result[0]["generated_text"]
            st.success("Estrategia IA generada:")
            st.write(estrategia_ia)
            
            # response = requests.post(api_url, headers=headers, json=payload)
            # if response.status_code == 200:
            #    output = response.json()
            #    estrategia_ia = output[0]["generated_text"]
            #    st.success("Estrategia IA generada:")
            #    st.write(estrategia_ia)
            # else:
            #    st.error(f"Error en Hugging Face API: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Error ejecutando el modelo: {e}")
else:
    st.info("Sube el Excel para continuar.")

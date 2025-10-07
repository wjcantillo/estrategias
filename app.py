import streamlit as st
import pandas as pd
import requests

st.title("Comparador de Estrategias BSC con IA")

BACKEND_URL = "https://huggingface.co/spaces/walbertocantillo>/bsc-estrategias-model/api/predict"

archivo = st.file_uploader("Sube tu Excel con el BSC", type=["xlsx"])

if archivo:
    df = pd.read_excel(archivo)
    st.dataframe(df)
    idx = st.number_input("Selecciona fila", 0, len(df)-1)
    objetivo = df.loc[idx, "Objetivo"]
    iniciativa = df.loc[idx, "Iniciativa"]

    if st.button("Generar estrategia con IA"):
        payload = {"data": [objetivo, iniciativa]}
        resp = requests.post(BACKEND_URL, json=payload)
        if resp.status_code == 200:
            estrategia = resp.json()["data"][0]
            st.success("Estrategia generada:")
            st.write(estrategia)
        else:
            st.error(f"Error en backend: {resp.text}")

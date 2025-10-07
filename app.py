import streamlit as st
import pandas as pd
from gradio_client import Client

st.subheader("Comparador de Estrategias BSC con IA")

client = Client("walbertocantillo/bsc-estrategias-model")

archivo = st.file_uploader("Sube tu Excel con el BSC", type=["xlsx"])

if archivo:
    df = pd.read_excel(archivo)
    st.dataframe(df)
    idx = st.number_input("Selecciona fila", 0, len(df)-1)
    objetivo = df.loc[idx, "Objetivo"]
    iniciativa = df.loc[idx, "Iniciativa"]

    if st.button("Generar estrategia con IA"):
        try:
            # Llamada al backend Hugging Face
            result = client.predict(objetivo=objetivo, iniciativa=iniciativa, api_name="/predict")
            st.success("Estrategia generada:")
            st.write(result)
        except Exception as e:
            st.error(f"Error en backend: {e}")

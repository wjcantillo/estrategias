import streamlit as st
import pandas as pd
from transformers import pipeline

st.set_page_config(page_title="Generador de Estrategias BSC", layout="centered")
st.title("Generador de Estrategias del Balanced Scorecard (Optimizado)")

# Cargar modelo localmente (puede tardar la primera vez)
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="bigscience/bloomz-560m")

generator = load_model()

archivo = st.file_uploader("Sube tu archivo Excel con columnas: Perspectiva, Objetivo, Meta, Indicador, Iniciativa", type=["xlsx"])

if archivo:
    df = pd.read_excel(archivo)
    st.dataframe(df)

    index = st.number_input("Selecciona la fila:", 0, len(df)-1)
    objetivo = df.loc[index, "Objetivo"]
    iniciativa = df.loc[index, "Iniciativa"]

    if st.button("Generar Estrategia con IA"):
        prompt = f"""Eres un experto en planeación estratégica. 
Redacta en español **dos estrategias organizacionales** claras, concretas y medibles 
que relacionen la siguiente iniciativa con el cumplimiento del objetivo.

Objetivo: {objetivo}
Iniciativa: {iniciativa}

Estrategias:"""
        try:
            results = generator(prompt, max_length=300, min_length=100, temperature=0.7, top_p=0.9, do_sample=True, num_return_sequences=2)
            # estrategia_ia = result[0]["generated_text"].replace(prompt, "").strip()
            st.success("Estrategia IA generada:")
            for i, r in enumerate(results):
                estrategia_ia = r["generated_text"].replace(prompt, "").strip()
                st.markdown(f"### Estrategia {i+1}")
                st.write(estrategia_ia)
        
        except Exception as e:
            st.error(f"Error ejecutando el modelo: {e}")
else:
    st.info("Sube el Excel para continuar.")

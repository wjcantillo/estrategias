import streamlit as st
import pandas as pd
from transformers import pipeline

st.set_page_config(page_title="Generador de Estrategias BSC", layout="centered")
st.title("Generador de Estrategias del Balanced Scorecard (Optimizado)")

st.markdown("""
Sube tu archivo Excel con las columnas: **Perspectiva, Objetivo, Meta, Indicador, Iniciativa**  
Esta versión usa el modelo **`google/flan-t5-small`** para que funcione en Streamlit Cloud free.
""")

# Cargar modelo localmente (puede tardar la primera vez)
@st.cache_resource
def load_model():
    return pipeline("text2text-generation", model="google/flan-t5-small")

generator = load_model()

archivo = st.file_uploader("Sube tu archivo Excel con columnas: Perspectiva, Objetivo, Meta, Indicador, Iniciativa", type=["xlsx"])

if archivo:
    df = pd.read_excel(archivo)
    st.dataframe(df)

    index = st.number_input("Selecciona la fila:", 0, len(df)-1)
    objetivo = df.loc[index, "Objetivo"]
    iniciativa = df.loc[index, "Iniciativa"]

    if st.button("Generar Estrategia con IA"):
        prompt = f"""Tarea: Redactar en español una estrategia organizacional clara, concreta y medible
que relacione la siguiente iniciativa con el cumplimiento del objetivo.

Objetivo: {objetivo}
Iniciativa: {iniciativa}

Estrategia:"""
           
        try:
            result = generator(prompt, max_length=256)
            estrategia_ia = result[0]["generated_text"].replace(prompt, "").strip()
            st.success("Estrategia IA generada:")
            st.write(estrategia_ia)
        
        except Exception as e:
            st.error(f"Error ejecutando el modelo: {e}")
else:
    st.info("Sube el Excel para continuar.")

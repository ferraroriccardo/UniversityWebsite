import streamlit as st
from utils.utils import *
import pandas as pd


def struct(connection=None):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Quaderno 4 :blue[Basi di Dati]")
    with col2:
        st.image("images/polito_white.png")

    st.markdown("### Riccardo Ferraro s299845")
    st.markdown("## :blue[Obiettivo]")
    st.markdown(
        '_Creare un’applicazione web in Python (Streamlit) in grado di interagire con un database MySQL in modo da eseguire interrogazioni in base alle interazioni dell’utente_')

    try:
        queryOre = "SELECT OraInizio, COUNT(*) AS nLezioni FROM Programma GROUP BY OraInizio"
        val = execute_query(connection, queryOre)
        df = pd.DataFrame(val.fetchall(), columns=val.keys())
        st.bar_chart(df, x='OraInizio', y='nLezioni')
    except Exception as e:
        st.error("Connettit al DB per visualizzare i dati.")

        st.markdown("### Giorno della settimana")
    try:
        val1 = execute_query(connection, "SELECT Giorno, SUM(Durata) FROM Programma GROUP BY Giorno")
        df = pd.DataFrame(val1.fetchall(), columns=val1.keys())
        df['SUM(Durata)'] = df['SUM(Durata)'].astype(float)  # Converti 'SUM(Durata)' in float
        st.area_chart(df, x='Giorno', y='SUM(Durata)')

    except Exception as e:
        st.error("Connettit al DB per visualizzare i dati.")



if __name__ == '__main__':
    st.set_page_config(
        page_title="Quaderno 4",
        layout="wide",
        page_icon="📚",
        initial_sidebar_state="expanded"
    )
    if check_connection():
        try:
            struct(connection=st.session_state["connection"])
        except:
            pass
    else:
        struct()
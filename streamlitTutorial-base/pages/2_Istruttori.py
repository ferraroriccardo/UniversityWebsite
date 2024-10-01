import streamlit as st
import pandas as pd

from utils.utils import *
from datetime import datetime


def struct(connection=None):
    col1, col2 = st.columns([3, 1])
    try:
        with col1:
            st.title("Visualizzazione Istruttori Disponibili")
            st.markdown("---")
            istrQuery = "SELECT * FROM Istruttore"
            istruttori = execute_query(connection, istrQuery)

            df = pd.DataFrame(istruttori.fetchall(), columns=istruttori.keys())

            df["DataNascita"] = pd.to_datetime(df["DataNascita"])

            # Sidebar filters
            cognome_filter = st.sidebar.text_input("Cognome dell'Istruttore")
            data_nascita_start = st.sidebar.date_input("Data di Nascita (Inizio)", datetime(1970, 1, 1))
            data_nascita_end = st.sidebar.date_input("Data di Nascita (Fine)", datetime(2000, 12, 31))

            # Apply filters
            if cognome_filter:
                df = df[df["Cognome"].str.contains(cognome_filter, case=False, na=False)]
            df = df[(df["DataNascita"] >= pd.to_datetime(data_nascita_start)) & (
                        df["DataNascita"] <= pd.to_datetime(data_nascita_end))]

            # Display results
            if not df.empty:
                st.markdown(f"## {int(df.size / len(df.columns))} Risultati ")
                for index, row in df.iterrows():
                    st.markdown(
                        f"""
                    <div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px;">
                        <h4> {row['Nome']} {row['Cognome']}</h4>
                        <p> Codice Fiscale:  {row['CodFisc']} </p>
                        <p> Data di Nascita: {row['DataNascita'].strftime('%Y-%m-%d')} </p>
                        <p> Email: {row['Email']} </p>
                        <p> Telefono: {row['Telefono']}</p>
                    </div>
                    """,
                        unsafe_allow_html=True
                    )
                    st.write("---")
            else:
                st.write("Nessun istruttore trovato per i criteri di ricerca specificati.")
        with col2:
            st.image("https://didattica.polito.it/img/logo_poli/logo_poli_bianco_260.png", width=300)
    except Exception as e:
        print(e)
        st.error("Connettiti al DB per visualizzare i dati.")


if __name__ == '__main__':
    st.set_page_config(
        page_title="Quaderno 4",
        layout="wide",
        page_icon="📚",
        initial_sidebar_state="expanded"
    )
    st.logo("https://didattica.polito.it/img/logo_poli/logo_poli_bianco_260.png")

    if check_connection():
        try:
            conn = connect_db(dialect="mysql+pymysql", username="root", password="mypassword", host="localhost",
                              dbname="palestra")
            struct(connection=conn)
        except:
            pass
    else:
        struct()
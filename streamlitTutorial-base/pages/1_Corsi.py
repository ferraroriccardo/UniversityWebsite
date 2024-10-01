import streamlit as st
import pandas as pd
from utils.utils import *


def informazioni_corsi(conn):
    queryNCorsi = "SELECT COUNT(*) FROM Corsi"
    queryTipiCorsi = "SELECT DISTINCT Tipo FROM Corsi"

    nCorsi = execute_query(conn, queryNCorsi)
    dfnCorsi = pd.DataFrame(nCorsi.fetchall(), columns=nCorsi.keys())

    tipoCorsi = execute_query(conn, queryTipiCorsi)
    dftipoCorsi = pd.DataFrame(tipoCorsi.fetchall(), columns=tipoCorsi.keys())

    return dfnCorsi, dftipoCorsi


def mostra_corsi(dfnCorsi, dftipoCorsi):
    st.metric("Corsi disponibili", dfnCorsi["COUNT(*)"][0])
    st.metric("Tipi di corsi", len(dftipoCorsi))
    st.write("### Tipi di corsi")
    for index, row in dftipoCorsi.iterrows():
        st.write(f" - {row['Tipo']}")


def mostra_filtrati(conn, dftipoCorsi):
    with st.expander("Filtra tipo corso"):
        tipo = st.selectbox("Scegli il tipo di corso", dftipoCorsi["Tipo"])
        query = f"""
        SELECT Istruttore.Nome as NomeIstruttore, Istruttore.Cognome, Corsi.Nome  
        FROM Corsi
        INNER JOIN Programma ON Programma.CodC = Corsi.CodC
        INNER JOIN Istruttore ON Programma.CodFisc = Istruttore.CodFisc
        WHERE Corsi.Tipo = '{tipo}'
        """
        val = execute_query(conn, query)
        df = pd.DataFrame(val.fetchall(), columns=val.keys())
        for i in range(len(df)):
            st.write(f" - :red[{df.iloc[i]['Nome']}] : {df.iloc[i]['NomeIstruttore']} {df.iloc[i]['Cognome']}")


def struct(connection=None):
    """Crea l'interfaccia utente e visualizza i dati."""
    col1, col2 = st.columns([1, 1])
    try:
        with col1:
            dfnCorsi, dftipoCorsi = informazioni_corsi(connection)
            mostra_corsi(dfnCorsi, dftipoCorsi)
        with col2:
            st.image("https://didattica.polito.it/img/logo_poli/logo_poli_bianco_260.png", width=300)
            st.markdown("---")
            mostra_filtrati(connection, dftipoCorsi)
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
            struct(connection=st.session_state["connection"])
        except:
            pass
    else:
        struct()
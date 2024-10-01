import streamlit as st
import pandas as pd
from utils.util import *


def check_info(prod_dict):
    for value in prod_dict.values():
        if value == '':
            return False
    return True


def exec_query(connection, query):
    try:
        execute_query(connection, query)
        connection.commit()
    except Exception as e:
        st.error(e)
        return False
    return True


def insert_db(prod_dict, connect):
    if check_info(prod_dict):
        attributi = ", ".join(prod_dict.keys())
        valori = tuple(prod_dict.values())
        query = f"INSERT INTO Programma ({attributi}) VALUES {valori};"
        return exec_query(connect, query)
    return False


def pick_CodF(connection):
    query = "SELECT CodFisc FROM Istruttore"
    istruttori = execute_query(connection, query)
    df = pd.DataFrame(istruttori)
    return st.selectbox("Seleziona il Codice Fiscale dell'istruttore:", df)


def pick_codC(connection):
    query = "SELECT CodC ,Nome ,Livello  FROM Corsi"
    corsi = execute_query(connection, query)
    df = pd.DataFrame(corsi)
    tipo = st.selectbox("Seleziona il tipo di corso:", df['Nome'])
    return df[df['Nome'] == tipo]['CodC'].values[0]


def crea_form(connection):
    try:
        CodFisc = pick_CodF(connection)
        codC = pick_codC(connection)
    except Exception as e:
        st.error(e)
        return
    durata = st.slider(label="Durata del corso", min_value=10, max_value=60)
    giorno = st.selectbox("Giorno", ("Lunedì", "Martedì", "Mercoledì", 'Giovedì', "Venerdì"))
    ora = st.slider(label="Ora", min_value=6, max_value=23)
    minuti = st.slider(label="Minuti", min_value=0, max_value=30, step=30)
    orario = f'{ora}:{minuti if minuti == 30 else str(minuti) + "0"}:00'
    sala = st.text_input("Inserire la sala")
    return {
        "CodFisc": CodFisc,
        "Giorno": giorno,
        "OraInizio": orario,
        "Durata": durata,
        "Sala": sala,
        "CodC": codC
    }


def check_lesson(connection, dict):
    query = f'''
    SELECT CodC
    FROM Programma
    WHERE Giorno = "{dict["Giorno"]}" 
    '''
    cod = execute_query(connection, query)
    df = pd.DataFrame(cod)
    if (df["CodC"] == dict["CodC"]).any():
        st.error("Lezione già presente in questo giorno", icon='⚠️')
        return False
    return True


def struct(connection=None):
    if connection:
        with st.form("Inserimento lezione"):
            st.header(":blue[Inserimento Lezione]")
            prod_dict = crea_form(connection)
            button = st.form_submit_button("Inserire lezione", type='primary')
            if button:
                try:
                    if check_lesson(connection, prod_dict):
                        if insert_db(prod_dict, connection):
                            st.success("Lezione inserita con successo", icon='✅')
                            st.write(prod_dict)
                        else:
                            st.error("Errore nell'inserimento della lezione", icon='⚠️')
                except Exception as e:
                    st.error(e)
    else:
        st.error("Errore di connessione al database: Connettiti per poter inserire una lezione")


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
            struct(connection = st.session_state["connection"])
        except:
            pass
    else:
        struct()
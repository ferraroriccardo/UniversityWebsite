import streamlit as st
from utils.utils import *


#controlla se tutti i campi testuali sono stati riempiti
def check_info(prod_dict):
    for value in prod_dict.values():
        if value=='':
            return False
    return True


# #inserisce il nuovo prodotto
def insert_db(prod_dict, connect):
    if check_info(prod_dict):
        attributi=", ".join(prod_dict.keys())
        valori=tuple(prod_dict.values())
        query=f"INSERT INTO Istruttore ({attributi}) VALUES {valori};"
        try:
            execute_query(connect,query)
            connect.commit()
        except Exception as e:
            st.error(e)
            return False
        return True
    else:
        return False


def pick_information(connection):
    query = "SELECT * FROM Istruttore"
    istruttori = execute_query(connection, query)
    return istruttori.keys()

def inserimento_dati():
        CodFisc = st.text_input("Codice Fiscale", placeholder="Inserire il codice fiscale")
        Nome = st.text_input("Nome", placeholder = "Inserire il nome")
        Cognome = st.text_input("Cognome", placeholder = "Inserire il cognome")
        DataNascita = st.date_input("Data di Nascita")
        Email = st.text_input("Email", placeholder = "Inserire l'email")
        telefono = st.text_input("Telefono*", placeholder = "Inserire il numero di telefono")
        return {
            "CodFisc": CodFisc ,
            "Nome": Nome,
            "Cognome": Cognome,
            "DataNascita": str(DataNascita),
            "Email": Email,
            "Telefono": telefono if telefono else "NULL"
        }

def struct (connection = None):
    with st.form("Nuovo Istruttore"):
        st.header(":blue[Aggiungi istruttore:]")
        insert_dict = inserimento_dati()
        submitted=st.form_submit_button("Conferma",type='primary')
        if submitted:
            if insert_db(insert_dict, connect = connection) and connection is not None:
                st.success("Hai inserito questo istruttore: ",icon='✅')
                st.write(insert_dict)
            else:
                st.error("Impossibile aggiungere l'istruttore.",icon='⚠️')



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
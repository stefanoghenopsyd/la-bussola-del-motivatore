import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random

# --- 1. CONFIGURAZIONE E TESTI ---
st.set_page_config(page_title="Bussola Motivazionale - GENERA", layout="centered")

FACTORS = {
    "Premi e Punizioni": "Estrinseco",
    "Responsabilità e Competenza": "Ibrido Intr/Est",
    "Interesse e Senso del Dovere": "Intrinseco",
    "Appartenenza e Comunità": "Ibrido Intr/Clima",
    "Qualità delle Relazioni": "Clima",
    "Informazioni Disponibili": "Ibrido Clima/Est",
    "Talenti e Attitudini": "Intrinseco"
}

# Definizione dei 14 items basati sui punti di attenzione
QUESTIONS = [
    {"id": "q1", "text": "Mi assicuro che premi e sanzioni siano distribuiti con equità tra i collaboratori.", "factor": "Premi e Punizioni"},
    {"id": "q2", "text": "Valuto con oggettività le prestazioni prima di assegnare incentivi.", "factor": "Premi e Punizioni"},
    {"id": "q3", "text": "Offro ai miei collaboratori compiti che ne accrescano la responsabilità.", "factor": "Responsabilità e Competenza"},
    {"id": "q4", "text": "Incentivo percorsi di formazione per sviluppare nuove competenze nel team.", "factor": "Responsabilità e Competenza"},
    {"id": "q5", "text": "Condivido costantemente informazioni rilevanti sull'andamento aziendale.", "factor": "Informazioni Disponibili"},
    {"id": "q6", "text": "Mi accerto che ogni collaboratore abbia i dati necessari per svolgere il suo lavoro.", "factor": "Informazioni Disponibili"},
    {"id": "q7", "text": "Intervengo attivamente per gestire i conflitti in modo costruttivo.", "factor": "Qualità delle Relazioni"},
    {"id": "q8", "text": "Dedico tempo a curare le relazioni personali e professionali tra i colleghi.", "factor": "Qualità delle Relazioni"},
    {"id": "q9", "text": "Promuovo iniziative che rafforzino il senso di appartenenza al gruppo.", "factor": "Appartenenza e Comunità"},
    {"id": "q10", "text": "Lavoro affinché i valori aziendali siano condivisi e sentiti da tutti.", "factor": "Appartenenza e Comunità"},
    {"id": "q11", "text": "Assegno i compiti basandomi sui talenti naturali dei miei collaboratori.", "factor": "Talenti e Attitudini"},
    {"id": "q12", "text": "Cerco di allineare le sfide lavorative alle attitudini individuali.", "factor": "Talenti e Attitudini"},
    {"id": "q13", "text": "Sottolineo l'importanza del senso del dovere verso l'oggetto del lavoro.", "factor": "Interesse e Senso del Dovere"},
    {"id": "q14", "text": "Cerco di trasmettere passione e amore per la qualità del lavoro svolto.", "factor": "Interesse e Senso del Dovere"}
]

# --- 2. LOGICA DI SALVATAGGIO ---
def save_to_drive(data):
    try:
        # Caricamento credenziali da st.secrets [cite: 20]
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
        client = gspread.authorize(creds)
        sheet = client.open("Database_Motivazione").sheet1
        sheet.append_row(data)
    except Exception as e:
        st.warning("Nota: I dati non sono stati salvati sul database online, ma il tuo feedback è pronto!")

# --- 3. INTERFACCIA UTENTE ---
st.image("GENERA Logo Colore.png", width=300) # 
st.title("La Tua Bussola Motivazionale")

st.markdown("""
### Introduzione
La motivazione al lavoro è un sistema integrato dove convivono tre macroaree: **Fattori Intrinseci, Estrinseci e di Clima**. 
Sebbene ogni fattore eserciti un'influenza diversa, un buon motivatore deve saper agire su tutte queste leve. 
Questa autovalutazione ti aiuterà a scoprire la tua **'bussola' personale**, riconoscendo quali leve utilizzi con maggior frequenza.
""")

with st.form("survey_form"):
    st.subheader("Informazioni Socio-Anagrafiche")
    nome = st.text_input("Nome o Nickname")
    genere = st.selectbox("Genere", ["maschile", "femminile", "non binario", "non risponde"])
    eta = st.selectbox("Età", ["fino a 20 anni", "21-30 anni", "31-40 anni", "41-50 anni", "51-60 anni", "61-70 anni", "più di 70 anni"])
    studio = st.selectbox("Titolo di studio", ["licenza media", "qualifica professionale", "diploma di maturità", "laurea triennale", "laurea magistrale", "titolo post lauream"])
    ruolo = st.selectbox("Ruolo professionale", ["imprenditore", "top manager", "middle manager", "impiegato", "operaio", "tirocinante", "libero professionista"])

    st.subheader("Questionario")
    st.info("Valuta quanto ti rivedi in queste affermazioni (1 = Per nulla, 6 = Completamente)")
    
    # Shuffle delle domande
    if 'shuffled_questions' not in st.session_state:
        st.session_state.shuffled_questions = random.sample(QUESTIONS, len(QUESTIONS))
    
    responses = {}
    for q in st.session_state.shuffled_questions:
        responses[q['id']] = st.slider(q['text'], 1, 6, 3)

    submit = st.form_submit_button("Genera Feedback")

if submit:
    # Calcolo punteggi per fattore
    scores = {f: 0 for f in FACTORS.keys()}
    for q in QUESTIONS:
        scores[q['factor']] += responses[q['id']]
    
    # Identificazione orientamento dominante
    top_factors = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:2]
    
    # --- VISUALIZZAZIONE RISULTATI ---
    st.header("Il Tuo Orientamento")
    
    # Grafico (Esempio Radar/Bussola semplificato)
    fig, ax = plt.subplots(figsize=(6, 6))
    categories = list(scores.keys())
    values = list(scores.values())
    ax.barh(categories, values, color='#1f77b4') # Usa colori dal logo GENERA se noti
    st.pyplot(fig)

    st.write(f"**Il tuo orientamento prevalente è focalizzato su: {top_factors[0][0]} e {top_factors[1][0]}.**")
    st.write("Questo indica una propensione a motivare i collaboratori agendo principalmente su leve di tipo " + 
             f"{FACTORS[top_factors[0][0]]}. Ricorda che un sistema motivazionale efficace integra tutte le dimensioni.")

    # Preparazione dati per Drive
    row = [nome, genere, eta, studio, ruolo] + [responses[f"q{i+1}"] for i in range(14)]
    save_to_drive(row)

st.markdown("---")
st.markdown("<center>Powered by GÉNERA</center>", unsafe_allow_html=True)

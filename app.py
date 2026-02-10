import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random

# --- 1. CONFIGURAZIONE E MAPPATURA ---
st.set_page_config(page_title="Bussola Motivazionale - GENERA", layout="centered")

# Mappatura dei fattori sui 4 orientamenti (Punti Cardinali)
# NORD: Regole e Valori (Leader Ispiratore)
# SUD: Relazioni e Appartenenza (Gestore del Clima)
# EST: Competenze e Talenti (Coach Evolutivo)
# OVEST: Premi e Informazione (Manager Strutturale)

QUESTIONS = [
    {"id": "q1", "text": "Mi assicuro che premi e sanzioni siano distribuiti con equità.", "axis": "WEST", "factor": "Premi/Punizioni"},
    {"id": "q2", "text": "Valuto con oggettività le prestazioni prima di assegnare incentivi.", "axis": "WEST", "factor": "Premi/Punizioni"},
    {"id": "q3", "text": "Offro ai miei collaboratori compiti che ne accrescano la responsabilità.", "axis": "EAST", "factor": "Competenze"},
    {"id": "q4", "text": "Incentivo percorsi di formazione per sviluppare nuove competenze.", "axis": "EAST", "factor": "Competenze"},
    {"id": "q5", "text": "Condivido costantemente informazioni rilevanti sull'andamento aziendale.", "axis": "WEST", "factor": "Informazione"},
    {"id": "q6", "text": "Mi accerto che ogni collaboratore abbia i dati necessari per lavorare.", "axis": "WEST", "factor": "Informazione"},
    {"id": "q7", "text": "Intervengo attivamente per gestire i conflitti in modo costruttivo.", "axis": "SOUTH", "factor": "Relazioni"},
    {"id": "q8", "text": "Dedico tempo a curare le relazioni personali nel team.", "axis": "SOUTH", "factor": "Relazioni"},
    {"id": "q9", "text": "Promuovo iniziative che rafforzino il senso di comunità.", "axis": "SOUTH", "factor": "Appartenenza"},
    {"id": "q10", "text": "Lavoro affinché i valori aziendali siano sentiti da tutti.", "axis": "NORTH", "factor": "Valori"},
    {"id": "q11", "text": "Assegno i compiti basandomi sui talenti naturali dei collaboratori.", "axis": "EAST", "factor": "Talenti"},
    {"id": "q12", "text": "Cerco di allineare le sfide lavorative alle attitudini individuali.", "axis": "EAST", "factor": "Talenti"},
    {"id": "q13", "text": "Sottolineo l'importanza del senso del dovere verso il lavoro.", "axis": "NORTH", "factor": "Dovere"},
    {"id": "q14", "text": "Condivido con i collaboratori le regole e i valori aziendali chiaramente.", "axis": "NORTH", "factor": "Valori"}
]

def plot_compass(scores):
    # Calcolo coordinate (X = Est - Ovest, Y = Nord - Sud)
    x = (scores['EAST'] / 4) - (scores['WEST'] / 4)
    y = (scores['NORTH'] / 3) - (scores['SOUTH'] / 4) # Normalizzato sul num. domande

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'projection': 'polar'})
    
    # Decorazione Bussola
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids([0, 90, 180, 270], ['NORD\nLeader Ispiratore', 'EST\nCoach Evolutivo', 'SUD\nGestore del Clima', 'OVEST\nManager Strutturale'])
    
    # Calcolo angolo e modulo per la lancetta
    angle = np.arctan2(x, y)
    distance = np.sqrt(x**2 + y**2)
    
    # Disegno lancetta (stile bussola)
    ax.annotate('', xy=(angle, distance), xytext=(0, 0),
                arrowprops=dict(facecolor='#E63946', edgecolor='black', width=5, headwidth=15))
    
    ax.set_ylim(0, 6) # Scala Likert max
    ax.set_yticklabels([]) # Nascondi cerchi concentrici numerici
    return fig

# --- 2. UI STREAMLIT ---
# Logo centrato
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("GENERA Logo Colore.png", width=250)

st.markdown("<h1 style='text-align: center;'>Bussola dell'Orientamento Motivazionale</h1>", unsafe_allow_html=True)

st.markdown("""
### La Motivazione come Sistema
La motivazione al lavoro non è un interruttore acceso/spento, ma un sistema in cui si integrano tre macroaree: **Fattori Intrinseci, Estrinseci e di Clima**. 
Un buon leader deve saper usare tutte le leve a disposizione. Questa autovalutazione ti aiuta a riconoscere la tua **"bussola" personale**: l'orientamento che guida il tuo modo di motivare i collaboratori.
""")

with st.form("survey_form"):
    st.subheader("Anagrafica")
    nome = st.text_input("Nome o Nickname")
    genere = st.selectbox("Genere", ["maschile", "femminile", "non binario", "non risponde"])
    eta = st.selectbox("Età", ["fino a 20 anni", "21-30 anni", "31-40 anni", "41-50 anni", "51-60 anni", "61-70 anni", "più di 70 anni"])
    studio = st.selectbox("Titolo di studio", ["licenza media", "qualifica professionale", "diploma di maturità", "laurea triennale", "laurea magistrale", "titolo post lauream"])
    ruolo = st.selectbox("Ruolo professionale", ["imprenditore", "top manager", "middle manager", "impiegato", "operaio", "tirocinante", "libero professionista"])

    st.subheader("Questionario (Scala 1-6)")
    if 'shuffled_items' not in st.session_state:
        st.session_state.shuffled_items = random.sample(QUESTIONS, len(QUESTIONS))
    
    answers = {}
    for item in st.session_state.shuffled_items:
        answers[item['id']] = st.select_slider(item['text'], options=[1,2,3,4,5,6], value=3)

    submit = st.form_submit_button("SCOPRI IL TUO ORIENTAMENTO")

if submit:
    # Calcolo punteggi per asse
    axis_scores = {"NORTH": 0, "SOUTH": 0, "EAST": 0, "WEST": 0}
    for item in QUESTIONS:
        axis_scores[item['axis']] += answers[item['id']]
    
    # Visualizzazione Feedback
    st.header("Il tuo Profilo Motivazionale")
    
    # Mostra la bussola
    st.pyplot(plot_compass(axis_scores))
    
    # Logica feedback testuale
    main_axis = max(axis_scores, key=axis_scores.get)
    orientations = {
        "NORTH": ("Leader Ispiratore", "Ti orienti verso la condivisione di valori e del senso del dovere. Motivi attraverso l'esempio e l'identificazione con la missione aziendale."),
        "SOUTH": ("Gestore del Clima", "Il tuo punto di forza è la cura delle relazioni e del senso di appartenenza. Crei un ambiente in cui le persone si sentono parte di una comunità."),
        "EAST": ("Coach Evolutivo", "Punti sullo sviluppo delle competenze e sulla valorizzazione dei talenti. Motivi offrendo sfide e autonomia."),
        "WEST": ("Manager Strutturale", "Ti assicuri che il sistema sia equo, le informazioni chiare e i premi distribuiti correttamente. Crei la struttura necessaria per operare bene.")
    }
    
    name_orient, desc_orient = orientations[main_axis]
    st.subheader(f"Sei un: {name_orient}")
    st.info(desc_orient)
    
    # Salvataggio dati (Identificativo, Genere, Età, Studio, Job, 14 items)
    row = [nome, genere, eta, studio, ruolo] + [answers[f"q{i+1}"] for i in range(14)]
    # Qui inseriresti la funzione save_to_drive(row) come discusso precedentemente

st.markdown("<br><hr><center>Powered by GÉNERA</center>", unsafe_allow_html=True)

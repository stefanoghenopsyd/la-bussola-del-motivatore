import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Bussola della Motivazione", layout="centered")

# --- HEADER: LOGO E TITOLO ---
# Nota: Il file "GENERA Logo Colore.png" deve essere nella stessa cartella del file .py
st.image("GENERA Logo Colore.png", width=300)
st.title("La Tua Bussola della Motivazione")

# --- INTRODUZIONE ---
st.markdown("""
### La Motivazione come Sistema Dinamico
La motivazione al lavoro non è un elemento statico, ma un **sistema integrato** dove convivono, influenzandosi vicendevolmente, tre macro aree di fattori: 
* **Intrinseci:** la spinta che nasce dentro di noi: dal piacere e dal dovere.
* **Estrinseci:** le leve esterne: i premi e la struttura delle regole.
* **di Clima:** l'ossigeno delle relazioni e della comunità.

Un buon leader deve saper orchestrare queste leve che hanno pesi differenti per le diverse persone. Questa autovalutazione ti aiuterà a riconoscere la tua **"bussola" personale** e a riflettere su come la usi per orientare il tuo team.
---
""")

# --- SEZIONE SOCIO-ANAGRAFICA ---
st.subheader("📋 Informazioni Generali")
with st.expander("Inserisci i tuoi dati", expanded=True):
    nome = st.text_input("Nome o Nickname")
    genere = st.selectbox("Genere", ["maschile", "femminile", "non binario", "non risponde"])
    eta = st.selectbox("Età", ["fino a 20 anni", "21-30 anni", "31-40 anni", "41-50 anni", "51-60 anni", "61-70 anni", "più di 70 anni"])
    titolo = st.selectbox("Titolo di studio", ["licenza media", "qualifica professionale", "diploma di maturità", "laurea triennale", "laurea magistrale", "titolo post lauream"])
    ruolo = st.selectbox("Ruolo professionale", ["imprenditore", "top manager", "middle manager", "impiegato", "operaio", "tirocinante", "libero professionista"])

# --- QUESTIONARIO (14 ITEM) ---
st.subheader("🧠 Questionario di Autovalutazione")
st.info("Rispondi onestamente pensando a come agisci con i tuoi collaboratori (Scala 1-5)")

# Definizione item e fattori
items = [
    ("Sono capace di essere equo nel premiare e sanzionare (1/2)", "Estrinseci"),
    ("Richiamo esplicitamente i miei collaboratori alle conseguenze delle loro azioni in termini di sanzioni e di premi (2/2)", "Estrinseci"),
    ("Mi impegno a fondo nell'esplicitare le responsabilità ai miei collaboratori (1/2)", "Estrinseci/Intrinseci"),
    ("Mi impegno a fondo sviluppare le competenze dei miei collaboratori (2/2)", "Estrinseci/Intrinseci"),
    ("Richiamo esplicitamente i miei collaboratori alle regole e ai valori da rispettare nel lavoro (1/2)", "Intrinseci"),
    ("Richiamo esplicitamente i miei collaboratori al senso del dovere (2/2)", "Intrinseci"),
    ("Mi impegno a fondo nel riconoscere le attitudini dei miei collaboratori e nel valorizzarne i talenti (1/2)", "Intrinseci"),
    ("Mi impegno a fondo nello stimolare l'interesse dei miei collaboratori verso il lavoro (2/2)", "Intrinseci"),
    ("Richiamo esplicitamente il valore dell'appartenenza al gruppo (1/2)", "Intrinseci/Clima"),
    ("Mi impegno a fondo nel promuovere il senso di comunità (2/2)", "Intrinseci/Clima"),
    ("Mi impegno a fondo nel curare le relazioni interpersonali (1/2)", "Clima"),
    ("Mi impegno a fondo nella gestione costruttiva dei conflitti (2/2)", "Clima"),
    ("Mi impegno a fondo nel fornire informazioni chiare e corrette (1/2)", "Clima/Estrinseci"),
    ("Sono attento a garantire trasparenza e accesso ai dati condivisi (2/2)", "Clima/Estrinseci")
]

responses = []
for desc, cat in items:
    val = st.slider(f"{desc}", 1, 5, 3)
    responses.append(val)

# --- LOGICA DI CALCOLO ---
if st.button("Genera Profilo"):
    # Aggregazione punteggi (Esempio semplificato di mapping)
    score_est = (responses[0] + responses[1] + responses[12] + responses[13]) / 4
    score_int = (responses[4] + responses[5] + responses[6] + responses[7]) / 4
    score_cli = (responses[8] + responses[9] + responses[10] + responses[11]) / 4

    # --- GRAFICO A BUSSOLA (Radar) ---
    categories = ['Estrinseci', 'Intrinseci', 'Clima']
    scores = [score_est, score_int, score_cli]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
          r=scores + [scores[0]],
          theta=categories + [categories[0]],
          fill='toself',
          name='Il tuo Profilo',
          line_color='teal'
    ))

    fig.update_layout(
      polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
      showlegend=False,
      title="La tua Bussola Motivazionale"
    )

    st.plotly_chart(fig)

    # --- FEEDBACK DESCRITTIVO ---
    st.subheader("🔍 Analisi dell'Orientamento")
    
    # Logica per determinare l'orientamento dominante
    max_val = max(scores)
    
    if score_est == score_int == score_cli:
        title = "L'Equilibratore Sistemico"
        desc = "Hai un approccio bilanciato: sai usare tutte le leve a tua disposizione in modo armonico."
    elif max_val == score_est:
        title = "Il Garante della Struttura"
        desc = "Il tuo orientamento è focalizzato sulla chiarezza, i risultati e l'equità dei processi."
    elif max_val == score_int:
        title = "L'Ispiratore di Senso"
        desc = "Punti sulla passione e sulla crescita interiore dei tuoi collaboratori."
    else:
        title = "Il Custode del Benessere"
        desc = "La tua priorità è l'armonia del gruppo e la qualità del legame umano."

    st.success(f"**Profilo Rilevato: {title}**")
    st.write(desc)

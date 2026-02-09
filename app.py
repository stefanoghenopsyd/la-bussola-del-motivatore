import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Bussola della Motivazione", layout="centered")

# --- HEADER: LOGO E TITOLO (Con gestione errore percorso) ---
try:
    # Cerca l'immagine nella stessa cartella dello script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(current_dir, "GENERA Logo Colore.png")
    st.image(logo_path, width=300)
except:
    # Se non trova l'immagine, mostra solo il testo (evita il crash)
    st.markdown("## GENERA")

st.title("La Tua Bussola della Motivazione")

# --- INTRODUZIONE ---
st.markdown("""
### La Motivazione come Sistema Dinamico
La motivazione al lavoro non è un elemento statico, ma un **sistema integrato** dove convivono tre macro aree: 
* **Intrinseci:** la spinta che nasce dentro di noi (piacere e dovere).
* **Estrinseci:** le leve esterne (premi e regole).
* **di Clima:** l'ossigeno delle relazioni e della comunità.

Un buon leader deve saper orchestrare queste leve. Questa autovalutazione ti aiuterà a riconoscere la tua **"bussola" personale**.
---
""")

# --- SEZIONE SOCIO-ANAGRAFICA ---
st.subheader("Informazioni Generali")
with st.expander("Inserisci i tuoi dati", expanded=True):
    nome = st.text_input("Nome o Nickname")
    genere = st.selectbox("Genere", ["maschile", "femminile", "non binario", "non risponde"])
    eta = st.selectbox("Età", ["fino a 20 anni", "21-30 anni", "31-40 anni", "41-50 anni", "51-60 anni", "61-70 anni", "più di 70 anni"])
    titolo = st.selectbox("Titolo di studio", ["licenza media", "qualifica professionale", "diploma di maturità", "laurea triennale", "laurea magistrale", "titolo post lauream"])
    ruolo = st.selectbox("Ruolo professionale", ["imprenditore", "top manager", "middle manager", "impiegato", "operaio", "tirocinante", "libero professionista"])

# --- QUESTIONARIO (14 ITEM) ---
st.subheader("Questionario di Autovalutazione")
st.info("Rispondi onestamente pensando a come agisci con i tuoi collaboratori (Scala 1-5)")

# Lista corretta degli Items
items = [
    # 0, 1: Estrinseci Puri
    ("Mi impegno a fondo nel premiare e sanzionare equamente i miei collaboratori", "Estrinseci"),
    ("Esplicito ai miei collaboratori le conseguenze positive e negative delle loro azioni", "Estrinseci"),
    
    # 2, 3: Ponte Estrinseci/Intrinseci (Responsabilità)
    ("Esplicito ai miei collaboratori le responsabilità che hanno", "Estrinseci/Intrinseci"),
    ("Mi impegno a far crescere e potenziare le competenze dei miei collaboratori", "Estrinseci/Intrinseci"),
    
    # 4, 5, 6, 7: Intrinseci Puri (Regole/Dovere + Amore/Interesse)
    ("Richiamo esplicitamente le regole e i valori da rispettare", "Intrinseci"),
    ("Richiamo esplicitamente i miei collaboratori al senso del dovere", "Intrinseci"),
    ("Mi impegno nel riconoscere le attitudini e valorizzare i talenti", "Intrinseci"),
    ("Stimolo l'interesse dei miei collaboratori verso il contenuto del lavoro", "Intrinseci"),
    
    # 8, 9: Ponte Intrinseci/Clima (Appartenenza)
    ("Richiamo esplicitamente il valore dell'appartenenza al gruppo", "Intrinseci/Clima"),
    ("Promuovo il senso di comunità, collaborazione e solidarietà", "Intrinseci/Clima"),
    
    # 10, 11: Clima Puro (Relazioni)
    ("Mi impegno a fondo nel curare le relazioni interpersonali", "Clima"),
    ("Mi impegno nella gestione costruttiva dei conflitti", "Clima"),
    
    # 12, 13: Ponte Clima/Estrinseci (Informazioni)
    ("Fornisco informazioni chiare e corrette", "Clima/Estrinseci"),
    ("Garantisco trasparenza e accesso ai dati condivisi", "Clima/Estrinseci")
]

responses = []
# Loop con chiave univoca per evitare errori di Streamlit
for i, (desc, cat) in enumerate(items):
    val = st.slider(f"{i+1}. {desc}", 1, 5, 3, key=f"item_{i}")
    responses.append(val)

# --- LOGICA DI CALCOLO ---
if st.button("Genera Profilo"):
    
    # LOGICA CORRETTA:
    # I fattori "ponte" contribuiscono a entrambe le aree adiacenti.
    
    # Estrinseci = Puri (0,1) + Ponte Resp (2,3) + Ponte Info (12,13)
    score_est = (responses[0] + responses[1] + responses[2] + responses[3] + responses[12] + responses[13]) / 6
    
    # Intrinseci = Puri (4,5,6,7) + Ponte Resp (2,3) + Ponte Appartenenza (8,9)
    score_int = (responses[4] + responses[5] + responses[6] + responses[7] + responses[2] + responses[3] + responses[8] + responses[9]) / 8
    
    # Clima = Puri (10,11) + Ponte Appartenenza (8,9) + Ponte Info (12,13)
    score_cli = (responses[10] + responses[11] + responses[8] + responses[9] + responses[12] + responses[13]) / 6

    # --- GRAFICO A BUSSOLA (Radar) ---
    categories = ['Estrinseci', 'Intrinseci', 'Clima']
    scores = [score_est, score_int, score_cli]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
          r=scores + [scores[0]], # Chiude il cerchio
          theta=categories + [categories[0]],
          fill='toself',
          name='Il tuo Profilo',
          line_color='#008080' # Verde acqua professionale
    ))

    fig.update_layout(
      polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
      showlegend=False,
      title="La tua Bussola Motivazionale"
    )

    st.plotly_chart(fig)

    # --- FEEDBACK DESCRITTIVO ---
    st.divider()
    st.subheader("🔍 Analisi dell'Orientamento")
    
    max_val = max(scores)
    # Calcolo della deviazione per capire se è bilanciato (se la differenza tra max e min è poca)
    is_balanced = (max(scores) - min(scores)) < 0.5 
    
    if is_balanced:
        title = "L'Equilibratore Sistemico"
        desc = "Hai un approccio multidimensionale. Riesci a passare con agilità dalla gestione del clima al dovere, senza dimenticare le regole. Il tuo orientamento è dinamico."
    elif max_val == score_est:
        title = "Il Garante della Struttura"
        desc = "Ti affidi alla chiarezza delle regole, all'equità dei premi e alla trasparenza. Sei un punto di riferimento solido, ma ricorda di curare anche l'aspetto emotivo."
    elif max_val == score_int:
        title = "L'Ispiratore di Senso"
        desc = "Punti sulla crescita del singolo, sulla passione e sul senso del dovere. Ti appassiona vedere le persone fiorire, ma attento a non dare per scontata la struttura."
    else:
        title = "Il Connettore Relazionale"
        desc = "Per te il team è una comunità. La tua forza è l'empatia e il clima armonioso. Assicurati però che le 'buone relazioni' non offuschino gli obiettivi e le regole."

    st.success(f"**Profilo Rilevato: {title}**")
    st.markdown(f"_{desc}_")

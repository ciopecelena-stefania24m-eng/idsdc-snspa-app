import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import streamlit.components.v1 as components

# =========================================================
# CONFIG PAGINĂ
# =========================================================
st.set_page_config(
    page_title="IDSDC - Platformă Academică SNSPA",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# DETECTARE TEMA STREAMLIT (LIGHT / DARK)
# =========================================================
theme_base = st.get_option("theme.base")

if theme_base == "dark":
    BG = "#0F172A"
    CARD = "#1E293B"
    TEXT = "#F8FAFC"
    SUBTEXT = "#94A3B8"
    PRIMARY = "#38BDF8"
    DANGER = "#F43F5E"
    SUCCESS = "#22C55E"
    BORDER = "#334155"
    PLOTLY_TEMPLATE = "plotly_dark"
else:
    BG = "#F8FAFC"
    CARD = "#FFFFFF"
    TEXT = "#0F172A"
    SUBTEXT = "#475569"
    PRIMARY = "#0284C7"
    DANGER = "#E11D48"
    SUCCESS = "#16A34A"
    BORDER = "#CBD5E1"
    PLOTLY_TEMPLATE = "plotly_white"

# =========================================================
# CSS GLOBAL RESPONSIVE + LIGHT/DARK SUPPORT
# =========================================================
st.markdown(f"""
<style>

html, body, [class*="css"] {{
    font-family: 'Segoe UI', sans-serif;
}}

.stApp {{
    background-color: {BG};
    color: {TEXT};
}}

h1, h2, h3, h4, h5 {{
    color: {TEXT} !important;
}}

p, li, span, label, div {{
    color: {TEXT};
}}

.header-univ {{
    color: {PRIMARY} !important;
    font-weight: 800;
}}

.header-facultate {{
    color: {SUBTEXT} !important;
}}

div[data-testid="stMetricBlock"] {{
    background-color: {CARD};
    border-radius: 14px;
    padding: 20px;
    border: 1px solid {BORDER};
    box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
}}

div[data-testid="stMetricValue"] {{
    color: {TEXT};
}}

div[data-testid="stMetricLabel"] {{
    color: {SUBTEXT};
}}

.sol-card {{
    background-color: {CARD};
    border: 1px solid {BORDER};
    border-top: 5px solid {PRIMARY};
    border-radius: 14px;
    padding: 20px;
    height: 100%;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}}

textarea {{
    background-color: {CARD} !important;
    color: {TEXT} !important;
    border: 1px solid {BORDER} !important;
}}

[data-testid="stSidebar"] {{
    background-color: {CARD};
}}

.block-container {{
    padding-top: 1rem;
    padding-bottom: 1rem;
}}

@media (max-width: 768px) {{

    h1 {{
        font-size: 1.8rem !important;
        text-align: center !important;
    }}

    h2 {{
        font-size: 1.3rem !important;
    }}

    .block-container {{
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }}

    div[data-testid="stMetricBlock"] {{
        padding: 14px !important;
    }}

    .sol-card {{
        margin-bottom: 15px;
    }}
}}

</style>
""", unsafe_allow_html=True)

# =========================================================
# DIALOG BUN VENIT
# =========================================================
@st.dialog("👋 Ghid de Bun Venit")
def ghid():
    st.markdown("""
    ### Cum utilizezi aplicația?

    1. Selectează tipul de criză
    2. Modifică intensitatea riscului
    3. Analizează impactul financiar
    4. Vezi recomandările executive
    """)

    if st.button("Pornește aplicația"):
        st.rerun()

if "vizitat" not in st.session_state:
    st.session_state["vizitat"] = True
    ghid()

# =========================================================
# HEADER
# =========================================================
col1, col2 = st.columns([1, 4])

with col1:
    st.image(
        "https://upload.wikimedia.org/wikipedia/ro/thumb/4/43/SNSPA._sigla.svg/960px-SNSPA._sigla.svg.png",
        width=120
    )

with col2:
    st.markdown(
        "<h2 class='header-univ'>SNSPA</h2>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<h4 class='header-facultate'>Instrument Digital de Suport Decizional în Criză</h4>",
        unsafe_allow_html=True
    )

st.markdown(
    "<h1>🏛️ IDSDC - Simulator Academic de Criză</h1>",
    unsafe_allow_html=True
)

st.divider()

# =========================================================
# DATE
# =========================================================
if "df_baza" not in st.session_state:

    data = {
        "Activitate": [
            "A1 Analiză",
            "A2 Dezvoltare",
            "A3 QA",
            "A4 Deployment"
        ],
        "Durata_Initiala_Luni": [3, 4, 2, 1],
        "Cost_Initial_EUR": [100000, 200000, 80000, 50000],
        "Status": [
            "Finalizat",
            "În progres",
            "Planificat",
            "Planificat"
        ]
    }

    st.session_state["df_baza"] = pd.DataFrame(data)

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:

    st.markdown("## ⚙️ Simulator risc")

    tip_criza = st.selectbox(
        "Tip criză",
        [
            "Sanitară",
            "Economică",
            "Tehnologică",
            "Geopolitică"
        ]
    )

    intensitate = st.slider(
        "Intensitate",
        1.0,
        3.0,
        1.0,
        0.1
    )

    st.divider()

    st.markdown("### 📝 Agendă")

    agenda_html = f"""
    <textarea
        id="agenda"
        style="
            width:100%;
            height:180px;
            padding:10px;
            border-radius:10px;
            background:{CARD};
            color:{TEXT};
            border:1px solid {BORDER};
        "
        placeholder="Scrie notițe..."
    ></textarea>

    <script>
    const agenda = document.getElementById("agenda");

    agenda.value = localStorage.getItem("agenda_idsdc") || "";

    agenda.addEventListener("input", function() {{
        localStorage.setItem("agenda_idsdc", this.value);
    }});
    </script>
    """

    components.html(agenda_html, height=200)

# =========================================================
# MOTOR SIMULARE
# =========================================================
ponderi = {
    "Sanitară": {"timp": 0.8, "cost": 0.4},
    "Economică": {"timp": 0.3, "cost": 1.0},
    "Tehnologică": {"timp": 0.7, "cost": 0.6},
    "Geopolitică": {"timp": 1.0, "cost": 0.9}
}

wt = ponderi[tip_criza]["timp"]
wc = ponderi[tip_criza]["cost"]

df = st.session_state["df_baza"]

df["Durata_Simulata"] = (
    df["Durata_Initiala_Luni"] *
    (1 + ((intensitate - 1) * wt))
)

df["Cost_Simulat"] = (
    df["Cost_Initial_EUR"] *
    (1 + ((intensitate - 1) * wc))
)

# =========================================================
# TABS
# =========================================================
tab1, tab2, tab3 = st.tabs([
    "📊 Financiar",
    "📈 Grafice",
    "💡 Recomandări"
])

# =========================================================
# TAB 1
# =========================================================
with tab1:

    st.subheader("Date proiect")

    df_edit = st.data_editor(
        df,
        use_container_width=True
    )

    total_initial = df["Cost_Initial_EUR"].sum()
    total_simulat = df["Cost_Simulat"].sum()

    delta = total_simulat - total_initial

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Buget inițial",
        f"{total_initial:,.0f} €"
    )

    c2.metric(
        "Buget sub criză",
        f"{total_simulat:,.0f} €",
        f"+{delta:,.0f} €"
    )

    c3.metric(
        "Intensitate",
        f"{intensitate:.1f}/3.0"
    )

    st.dataframe(
        df,
        use_container_width=True
    )

# =========================================================
# TAB 2
# =========================================================
with tab2:

    st.subheader("Impact bugetar")

    fig1 = px.bar(
        df,
        x="Activitate",
        y=["Cost_Initial_EUR", "Cost_Simulat"],
        barmode="group",
        template=PLOTLY_TEMPLATE
    )

    fig1.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    st.subheader("Impact timp")

    fig2 = go.Figure()

    fig2.add_trace(
        go.Scatter(
            x=df["Activitate"],
            y=df["Durata_Initiala_Luni"],
            mode="lines+markers",
            name="Inițial"
        )
    )

    fig2.add_trace(
        go.Scatter(
            x=df["Activitate"],
            y=df["Durata_Simulata"],
            mode="lines+markers",
            name="Simulat"
        )
    )

    fig2.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# =========================================================
# TAB 3
# =========================================================
with tab3:

    st.subheader("Recomandări executive")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f"""
            <div class="sol-card">
                <h4>🔄 Agile</h4>
                <p>
                Ajustează sprinturile și prioritizează MVP-ul.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="sol-card">
                <h4>⚙️ Tehnic</h4>
                <p>
                Automatizare, backup și infrastructură cloud.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="sol-card">
                <h4>👥 HR</h4>
                <p>
                Protecția echipei și reducerea burnout-ului.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

st.divider()

st.caption("IDSDC © 2026 | SNSPA")

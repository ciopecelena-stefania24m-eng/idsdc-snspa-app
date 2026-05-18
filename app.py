import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import streamlit.components.v1 as components

# --- CONFIGURARE PAGINĂ PREMIUM ÎNTUNECATĂ ---
st.set_page_config(
    page_title="IDSDC - Platformă Academică SNSPA", 
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STILIZARE TOTALĂ PENTRU MEDIU ÎNTUNECAT ---
st.markdown("""
    <style>
    .stApp { background-color: #0F172A !important; }
    div.stMarkdown p, div.stMarkdown li, span, label { color: #F8FAFC !important; font-size: 16px; }
    h1 { color: #FFFFFF !important; font-family: 'Segoe UI', Roboto, sans-serif !important; font-weight: 800 !important; text-shadow: 0px 2px 4px rgba(0,0,0,0.5); }
    h2, h3, h4 { color: #38BDF8 !important; font-family: 'Segoe UI', Roboto, sans-serif !important; font-weight: 700 !important; margin-top: 15px !important; }
    .header-univ { color: #38BDF8 !important; font-weight: 800 !important; margin-bottom: 0px !important; }
    .header-facultate { color: #94A3B8 !important; font-weight: 600 !important; margin-top: 0px !important; }
    div[data-testid="stMetricBlock"] { background-color: #1E293B !important; padding: 20px !important; border-radius: 12px !important; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3) !important; border-left: 5px solid #38BDF8 !important; }
    div[data-testid="stMetricLabel"] > div { color: #94A3B8 !important; }
    div[data-testid="stMetricValue"] > div { color: #FFFFFF !important; }
    
    /* Stilizare carduri solutii */
    .sol-card {
        padding: 15px;
        border-radius: 10px;
        background-color: #1E293B;
        border-top: 4px solid #38BDF8;
        height: 100%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    </style>
""", unsafe_allow_html=True)

# --- POP-UP INTERACTIV DE SERVICIU ---
@st.dialog("👋 Ghid de Bun Venit: Cum folosești IDSDC?")
def ghid_onboarding():
    st.markdown("""
    Felicitări pentru accesarea *Instrumentului Digital de Suport Decizional în Criză (IDSDC)*, dezvoltat pentru lucrarea de dizertație.
    
    ### 🧭 Pași rapizi pentru simulare:
    1. *Pasul 1:* Selectează una dintre cele *6 tipologii de criză* din stânga.
    2. *Pasul 2:* Ajustează *Slider-ul de Intensitate* (1.0 - 3.0).
    3. *Pasul 3:* Modifică direct valorile din tabelul din Tab-ul 1 dacă dorești să testezi un alt buget.
    4. *Pasul 4:* Analizează graficele, tabelul Business și citește soluțiile generate dinamic în Tab-ul 3.
    """)
    if st.button("Am înțeles, pornește aplicația!", type="primary"):
        st.rerun()

if "vizitat" not in st.session_state:
    st.session_state["vizitat"] = True
    ghid_onboarding()

# --- ANTET ACADEMIC ---
col_logo, col_titlu = st.columns([1, 4])
with col_logo:
    st.image("https://upload.wikimedia.org/wikipedia/ro/thumb/4/43/SNSPA._sigla.svg/960px-SNSPA._sigla.svg.png", width=160)
with col_titlu:
    st.markdown("<h2 class='header-univ'>ȘCOALA NAȚIONALĂ DE STUDII POLITICE ȘI ADMINISTRATIVE (SNSPA)</h2>", unsafe_allow_html=True)
    st.markdown("<h4 class='header-facultate'>Facultatea de Management | Managementul Proiectelor | Lucrare de Disertație</h4>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; margin-top: 20px;'>🏛️ Instrument Digital de Suport Decizional în Criză (IDSDC)</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- DATE DE BAZĂ INIȚIALE ---
if "df_baza" not in st.session_state:
    data_initiala = {
        'Activitate': ['A1. Analiză & Arhitectură', 'A2. Dezvoltare Core Software', 'A3. Audit Securitate & QA', 'A4. Deployment & Infrastructură'],
        'Departament': ['Business Analysis & Strategy', 'Software Engineering Dept', 'Quality Assurance & CyberSec', 'Cloud DevOps & Operations'],
        'Durata_Initiala_Luni': [3.0, 4.0, 3.0, 2.0],
        'Cost_Initial_EUR': [100000.0, 200000.0, 120000.0, 80000.0],
        'Status': ['Finalizat', 'În Progres', 'Planificat', 'Planificat'],
        'Valoare_Dobandita_EV': [100000.0, 50000.0, 0.0, 0.0],
        'Cost_Actual_AC': [100000.0, 50000.0, 0.0, 0.0],
        'Numar_Oameni': [3, 8, 4, 2]
    }
    st.session_state["df_baza"] = pd.DataFrame(data_initiala)

# --- CONFIGURARE SCENARII DE CRIZĂ & AGENDĂ ÎN SIDEBAR ---
with st.sidebar:
    st.markdown("### ⚙️ SIMULATOR DE RISC")
    
    tip_criza = st.selectbox(
        "1. Selectează Tipologia Crizei:",
        ["Sanitară", "Economică", "Tehnologică", "Securitate / Geopolitică", "Energetică", "Criză de Personal (HR)"]
    )
    
    intensitate_criza = st.slider(
        "2. Intensitate Factor de Risc:",
        min_value=1.0, max_value=3.0, value=1.0, step=0.1
    )
    
    contexte_reale = {
        "Sanitară": "*Exemplu Real:* Pandemia COVID-19. Blocaje logistice și trecere forțată la WFH.",
        "Economică": "*Exemplu Real:* Hiperinflația globală și scumpirea licențelor software.",
        "Tehnologică": "*Exemplu Real:* Incidentul CrowdStrike sau atacuri cibernetice de tip Ransomware.",
        "Securitate / Geopolitică": "*Exemplu Real:* Blocaje comerciale internaționale, război, întreruperi de aprovizionare.",
        "Energetică": "*Exemplu Real:* Șocul prețurilor energetice din Europa. Facturi triple pentru Data Centers.",
        "Criză de Personal (HR)": "*Exemplu Real:* The Great Resignation. Demisii masive în bloc ale arhitecților cheie."
    }
    st.info(contexte_reale[tip_criza])
    
    with st.spinner("Se analizează matricea de risc..."):
        time.sleep(0.3)
        
    st.markdown("---")
    st.markdown("### 📝 Agendă Personală (Notițe)")
    
    agenda_html = """
    <div style="font-family: 'Segoe UI', sans-serif;">
        <textarea id="agenda_text" style="width: 100%; height: 180px; background-color: #1E293B; color: #F8FAFC; border: 1px solid #38BDF8; border-radius: 8px; padding: 10px; resize: vertical; outline: none; font-size: 14px;" placeholder="Ia notițe aici în timpul prezentării... (se salvează automat în memoria browserului)"></textarea>
        <script>
            const agenda = document.getElementById('agenda_text');
            // Incarcam notitele anterioare
            agenda.value = localStorage.getItem('idsdc_agenda_snspa') || '';
            // Salvam la fiecare apasare de tasta
            agenda.addEventListener('input', function() {
                localStorage.setItem('idsdc_agenda_snspa', this.value);
            });
        </script>
    </div>
    """
    # Acum componenta este integrată STRICT în sidebar
    components.html(agenda_html, height=210)

# Ponderi riscuri
ponderi = {
    "Sanitară": {"timp": 0.8, "cost": 0.3, "stres": 0.9},
    "Economică": {"timp": 0.2, "cost": 1.1, "stres": 0.6},
    "Tehnologică": {"timp": 0.7, "cost": 0.6, "stres": 0.8},
    "Securitate / Geopolitică": {"timp": 0.9, "cost": 0.8, "stres": 0.7},
    "Energetică": {"timp": 0.3, "cost": 1.0, "stres": 0.5},
    "Criză de Personal (HR)": {"timp": 1.2, "cost": 0.7, "stres": 1.0}
}

w_timp = ponderi[tip_criza]["timp"]
w_cost = ponderi[tip_criza]["cost"]
w_stres = ponderi[tip_criza]["stres"]

# --- DEFINIRE MOTOR DE SIMULARE ---
def executa_simulare(df, intensitate, wt, wc, ws):
    df_nou = df.copy()
    factor_timp = 1 + ((intensitate - 1) * wt)
    factor_cost = 1 + ((intensitate - 1) * wc)
    
    df_nou["Durata_Simulata_Luni"] = df_nou.apply(lambda r: r["Durata_Initiala_Luni"] if r["Status"] == "Finalizat" else r["Durata_Initiala_Luni"] * factor_timp, axis=1)
    df_nou["Cost_Simulat_EUR"] = df_nou.apply(lambda r: r["Cost_Initial_EUR"] if r["Status"] == "Finalizat" else r["Cost_Initial_EUR"] * factor_cost, axis=1)
    df_nou["Indice_Stres_Oameni"] = df_nou.apply(lambda r: 10.0 if r["Status"] == "Finalizat" else min(15.0 + ((intensitate - 1) * ws * 42), 100.0), axis=1)
    return df_nou

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Impact Financiar & Grafice", 
    "🔥 BOOM: Impact Resurse Umane", 
    "💡 Matrice Executivă de Soluții", 
    "📘 Ghid Metodologic"
])

# --- PIPELINE DE CALCUL ---
with tab1:
    st.markdown("### 📝 Pasul 1: Datele de Pornire ale Proiectului (Editor Live)")
    df_editat = st.data_editor(st.session_state["df_baza"], key="editor_baza", use_container_width=True)
    st.session_state["df_baza"] = df_editat

df_simulat = executa_simulare(df_editat, intensitate_criza, w_timp, w_cost, w_stres)

total_bac = df_editat["Cost_Initial_EUR"].sum()
cost_total_simulat = df_simulat["Cost_Simulat_EUR"].sum()
depasire_buget = cost_total_simulat - total_bac
timp_total_initial = df_editat["Durata_Initiala_Luni"].sum()
timp_total_simulat = df_simulat["Durata_Simulata_Luni"].sum()
intarziere_luni = timp_total_simulat - timp_total_initial
total_ev = df_editat["Valoare_Dobandita_EV"].sum()
total_ac = df_editat["Cost_Actual_AC"].sum()
cpi = total_ev / total_ac if total_ac > 0 else 1.0

stres_mediu = df_simulat[df_simulat["Status"] != "Finalizat"]["Indice_Stres_Oameni"].mean()
if pd.isna(stres_mediu): stres_mediu = 10.0

df_business = pd.DataFrame({
    'Activitate Proiect': df_editat['Activitate'],
    'Status': df_editat['Status'],
    'Buget Inițial': df_editat['Cost_Initial_EUR'],
    'Buget sub Criză': df_simulat['Cost_Simulat_EUR'],
    'Pierdere Extra (€)': df_simulat['Cost_Simulat_EUR'] - df_editat['Cost_Initial_EUR'],
    'Întârziere Adăugată': df_simulat['Durata_Simulata_Luni'] - df_editat['Durata_Initiala_Luni']
})

# --- MOTOR DE RECOMANDĂRI DINAMICE (STRUCTURĂ PE PILONI) ---
def obtine_matrice_solutii(tip, intensitate):
    if intensitate == 1.0:
        return {
            "titlu": "🟢 STARE NOMINALĂ - EXECUȚIE PREDICTIVĂ (WATERFALL)",
            "tip_alerta": "success",
            "agile": "*Menținerea Baseline-ului:* Proiectul se află în parametrii optimi aprobați inițial. Execuția continuă secvențial conform planului Waterfall.\n* *Monitorizare Standard:* Nu se impune trecerea la ceremoniile Scrum. Se menține ședința lunară de Steering Committee.",
            "tech": "*Stabilitate Operațională:* Nu sunt necesare modificări de infrastructură. Livrabilele trec prin porțile de calitate (Quality Gates) prestabilite.",
            "hr": "*Climat Organizațional Sigur:* Resursele sunt alocate corect. Indicele de eficiență a muncii este maxim, nefiind nevoie de intervenții HR."
        }
    
    if tip == "Sanitară":
        if intensitate <= 1.7:
            return {
                "titlu": "🟡 RISC MODERAT: CRIZĂ SANITARĂ (PREVENȚIE ȘI LEAN)",
                "tip_alerta": "info",
                "agile": "*Hibridizare Scrum:* Adaptarea ceremoniilor Agile (Daily Stand-up, Sprint Review) pentru a funcționa hibrid. Reducerea cadenței de livrare la 2 săptămâni pentru a absorbi fluctuațiile de personal.",
                "tech": "*Infrastructură Descentralizată:* Configurarea urgentă a VPN-urilor de rezervă pentru a susține vârfuri de trafic WFH (Work From Home). Limitarea accesului fizic în server room.",
                "hr": "*Rotația Echipelor (A/B):* Împărțirea fizică a departamentelor în două grupuri care nu se intersectează niciodată, asigurând redundanța operațională în caz de infectare."
            }
        elif intensitate <= 2.4:
            return {
                "titlu": "🟠 CRIZĂ SEVERĂ: ȘOC SANITAR (TRANZIȚIE FULL-AGILE REMOTE)",
                "tip_alerta": "warning",
                "agile": "*Tranziție Remote Agile:* Trecere imediată la modelul Scrum 100% distribuit. Daily Stand-up-urile se realizează exclusiv video, cu durata tăiată strict la 15 minute pentru a combate 'Zoom Fatigue'.",
                "tech": "*Migrarea în Cloud a Posturilor de Lucru:* Implementarea VDI (Virtual Desktop Infrastructure). Programatorii nu mai depind de hardware-ul de la birou, scriind cod direct în cloud-ul securizat.",
                "hr": "*Protocol de Redundanță (Shadowing):* Identificarea obligatorie a unui 'backup' (înlocuitor) pentru fiecare lider tehnic. În caz de spitalizare bruscă, proiectul nu se blochează."
            }
        else:
            return {
                "titlu": "🔴 IMPACT CATASTROFAL: LOCKDOWN TOTAL ȘI COLAPS MEDICAL",
                "tip_alerta": "error",
                "agile": "*Agile de Supraviețuire (Hard MVP):* Se taie din Product Backlog toate funcționalitățile noi. Scopul devine exclusiv menținerea codului existent online. Ședințele de rafinare se anulează.",
                "tech": "*Înghețarea Lansărilor (Deployment Freeze):* Interzicerea oricărui 'Push in Production'. Niciun cod nou nu mai este lansat pentru a evita căderea sistemelor când echipa de suport este indisponibilă.",
                "hr": "*Suport Psihologic și Asincronitate:* Trecerea la un program 100% asincron. Oamenii lucrează când pot (noaptea/dimineața devreme), pentru a putea îngriji familiile afectate. Evaluarea se face exclusiv pe task-ul livrat, nu pe orele pontate."
            }

    elif tip == "Economică":
        if intensitate <= 1.7:
            return {
                "titlu": "🟡 RISC MODERAT: INFLAȚIE ȘI PRESIUNI PE COSTURI",
                "tip_alerta": "info",
                "agile": "*Limitarea Scopului (Scope Control):* Creșterea vigilenței Product Owner-ului împotriva Scope Creep (adăugarea necontrolată de cerințe). Orice cerință nouă din partea clientului necesită bugetare separată.",
                "tech": "*Audit Software (Lean IT):* Analiza licențelor software utilizate de echipele de dezvoltare și renunțarea imediată la tool-urile premium nefolosite la capacitate maximă.",
                "hr": "*Managementul Orelor Suplimentare:* Limitarea severă a orelor suplimentare (Overtime) pentru a evita plata sporurilor salariale și protejarea fluxului de numerar (Cash Flow)."
            }
        elif intensitate <= 2.4:
            return {
                "titlu": "🟠 CRIZĂ SEVERĂ: RECESIUNE (AGILE COST-CUTTING)",
                "tip_alerta": "warning",
                "agile": "*Scurtarea Sprinturilor la 1 Săptămână:* Product Owner-ul analizează la fiecare 7 zile dacă livrabilul produs justifică bugetul consumat. Se implementează Burn-down charts măsurate direct în Euro, nu în Story Points.",
                "tech": "*Migrare Open-Source:* Trecerea imediată a instrumentelor scumpe de analiză către alternative Open-Source gratuite, acceptând temporar o scădere a confortului tehnic.",
                "hr": "*Înghețarea Consultanței Externe:* Rezilierea contractelor cu programatorii de tip B2B (freelancers/contractori) și re-distribuirea sarcinii către echipa internă stabilă de angajați."
            }
        else:
            return {
                "titlu": "🔴 IMPACT CATASTROFAL: BLOCAJ FINANCIAR / FALIMENT IMINENT",
                "tip_alerta": "error",
                "agile": "*Tăierea Radicală a Backlog-ului (50% De-Scoping):* Proiectul este amputat. Jumătate din pachetele de lucru neîncepute sunt anulate unilateral. Se livrează doar nucleul vital pentru a onora minimal contractul.",
                "tech": "*Conversia CapEx în OpEx:* Vânzarea echipamentelor fizice (servere proprii) și trecerea pe închiriere Cloud de avarie pentru a obține o injecție rapidă de lichiditate.",
                "hr": "*Restructurare Defensivă (Hiring Freeze & Merge):* Înghețarea totală a angajărilor. Contopirea echipelor de Dezvoltare cu cele de QA pentru a reduce dramatic numărul total de ore facturabile lunar."
            }
            
    elif tip == "Criză de Personal (HR)":
        if intensitate <= 1.7:
            return {
                "titlu": "🟡 RISC MODERAT: FLUCTUAȚIE DE PERSONAL (RETENȚIE)",
                "tip_alerta": "info",
                "agile": "*Transparență prin Kanban:* Vizualizarea clară a volumului de muncă pe un board Kanban. Se impun limite stricte de tip WIP (Work in Progress) pentru a preveni supraîncărcarea programatorilor eficienți.",
                "tech": "*Reducerea Banalității (Toil Reduction):* Automatizarea task-urilor administrative (ex: generarea rapoartelor de cod) care frustrează inginerii seniori și îi împing spre demisie.",
                "hr": "*Cross-Skilling Rapid:* Inițierea unor programe interne scurte de transfer de competențe. Analiștii A1 sunt învățați să execute sarcini ușoare de testare A3 pentru a echilibra efortul."
            }
        elif intensitate <= 2.4:
            return {
                "titlu": "🟠 CRIZĂ SEVERĂ: EXODUL CREIERELOR (AGILE KNOWLEDGE SHIFT)",
                "tip_alerta": "warning",
                "agile": "*Ajustarea Vitezei (Velocity Under Stress):* Când planifică Sprintul, Scrum Master-ul scade forțat volumul de muncă alocat echipei cu 20% pentru a stopa riscul de Burnout și demisii în lanț.",
                "tech": "*Pair Programming Forțat:* Programatorii scriu cod în perechi (câte 2 la un singur ecran/task). Dacă un om demisionează subit, expertiza și logica codului rămân la celălalt.",
                "hr": "*Intervenție Directă pe Climat:* Implementarea săptămânii de lucru comprimate de 4 zile (fără scăderi salariale) strict pe perioada de tensiune maximă a proiectului pentru a oferi recuperare psihologică."
            }
        else:
            return {
                "titlu": "🔴 IMPACT CATASTROFAL: COLAPSUL ECHIPELOR CHEIE",
                "tip_alerta": "error",
                "agile": "*Sistare și Stabilizare (Sprint Halt):* Oprirea oficială a dezvoltării curente timp de 2 săptămâni. Efortul se mută 100% pe documentarea codului existent înainte ca restul echipei să plece.",
                "tech": "*Injecție de Expertiză Turnaround:* Arhitectura software prea complexă este abandonată. Se implementează șabloane standardizate (Boilerplates) care pot fi preluate ușor de dezvoltatori externi juniori.",
                "hr": "*Activarea Fondului de Urgență (Retention Bonuses):* Aprobarea din partea Consiliului a unor prime financiare masive, garantate contractual, plătibile doar specialiștilor cheie rămași, condiționate de livrarea finală."
            }

    # Fallback generic pentru Tehnologic, Geopolitic și Energetic
    if intensitate <= 1.7:
        return {"titlu": f"🟡 RISC MODERAT ({tip.upper()})", "tip_alerta": "info", "agile": "*Planificare Defensivă:* Adăugarea de buffere de timp (marje de +15%) în calendarul curent pentru a absorbi deviațiile tehnice.", "tech": "*Mentenanță Preventivă:* Curățarea codului sursă vechi (Technical Debt) și executarea de backup-uri zilnice izolate.", "hr": "*Instruire:* Sesiuni rapide de pregătire a personalului tehnic privind noile riscuri de operare."}
    elif intensitate <= 2.4:
        return {"titlu": f"🟠 CRIZĂ SEVERĂ ({tip.upper()} - TRANZIȚIE AGILE)", "tip_alerta": "warning", "agile": "*Sprinturi de Stabilizare:* Oprirea dezvoltării noilor funcționalități (Feature Freeze). Sprinturile se dedică exclusiv securizării și refactorizării proiectului.", "tech": "*Automatizare și Cloud:* Implementarea procedurilor de Chaos Engineering pentru a testa rezistența serverelor. Mutarea sarcinilor grele în arhitecturi Cloud flexibile (Serverless).", "hr": "*Autonomie Locală:* Descentralizarea puterii de decizie. Echipele devin autonome și pot ocoli protocoalele lente pentru a remedia problemele urgente."}
    else:
        return {"titlu": f"🔴 IMPACT CATASTROFAL ({tip.upper()} - PLAN DE AVARIE)", "tip_alerta": "error", "agile": "*Anularea Roadmap-ului:* Roadmap-ul proiectului este aruncat. Se trece la Management de Avarie, operând decizii de la o oră la alta.", "tech": "*Disaster Recovery & Zero-Trust:* Activarea Planului de Recuperare (DRP). Izolarea completă a rețelelor, tăierea accesului extern (Zero-Trust) și migrarea în centre de date suverane, independente energetic sau politic.", "hr": "*Mobilizare de Supraviețuire:* Personalul cheie intră în modul de On-Call (gardă 24/7). Efortul este orientat strict pe salvarea bazei de date a clienților."}

solutii_curente = obtine_matrice_solutii(tip_criza, intensitate_criza)

# ---------------- TAB 1: AFIȘARE METRICI ȘI TABELE ----------------
with tab1:
    st.markdown("---")
    st.markdown("### 🎯 Pasul 2: Indicatori Globali sub Criză")
    col_f1, col_f2, col_f3 = st.columns(3)
    col_f1.metric("Buget Planificat Total (BAC)", f"{total_bac:,.0f} €")
    col_f2.metric("Buget Necesar sub Criză (EAC)", f"{cost_total_simulat:,.0f} €", f"+{depasire_buget:,.0f} € Pierdere" if depasire_buget > 0 else "0 €", delta_color="inverse")
    col_f3.metric("Noua Durată Estimată", f"{timp_total_simulat:.1f} luni", f"+{intarziere_luni:.1f} luni Întârziere" if intarziere_luni > 0 else "În grafic", delta_color="inverse")
    
    st.markdown("### 🔍 Evaluarea Diagnostică a Eficienței Financiare (CPI)")
    if cpi < 1.0:
        procent_pierdere = (1 - cpi) * 100
        st.error(f"*Indicele de Eficiență a Costului (CPI) este stabilit la {cpi:.2f}:* Înregistrăm o *pierdere de eficiență netă de {procent_pierdere:.1f}%*.")
    else:
        st.success(f"*Indicele de Eficiență a Costului (CPI) este optim: {cpi:.2f}:* Fiecare euro investit generează valoare deplină.")
    
    st.markdown("---")
    st.markdown("### 📋 Pasul 3: Tabel Explicit de Impact Economic")
    
    def coloreaza_pierderi_dark(val):
        if val > 0: return 'background-color: #7F1D1D; color: #FEE2E2; font-weight: bold;'
        return 'background-color: #064E3B; color: #D1FAE5;'

    st.dataframe(
        df_business.style.format({
            'Buget Inițial': '{:,.0f} €', 'Buget sub Criză': '{:,.0f} €',
            'Pierdere Extra (€)': '{:,.0f} €', 'Întârziere Adăugată': '{:.1f} luni'
        }).map(coloreaza_pierderi_dark, subset=['Pierdere Extra (€)', 'Întârziere Adăugată']),
        use_container_width=True
    )
    
    st.markdown("---")
    st.markdown("### 📊 Pasul 4: Vizualizarea Deviațiilor pentru Comisie")
    g_col1, g_col2 = st.columns(2)
    with g_col1:
        fig_buget_clar = px.bar(df_business, x='Activitate Proiect', y=['Buget Inițial', 'Buget sub Criză'], barmode='group', title='Comparație Bugetară Directă (€)', color_discrete_sequence=["#38BDF8", "#FB7185"], template="plotly_dark")
        fig_buget_clar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_buget_clar, use_container_width=True)
    with g_col2:
        fig_timp_clar = go.Figure()
        fig_timp_clar.add_trace(go.Scatter(x=df_editat['Activitate'], y=df_editat['Durata_Initiala_Luni'], mode='lines+markers', name='Durată Baseline', line=dict(color='#38BDF8', width=3), marker=dict(size=8)))
        fig_timp_clar.add_trace(go.Scatter(x=df_simulat['Activitate'], y=df_simulat['Durata_Simulata_Luni'], mode='lines+markers', name='Durată sub Criză', line=dict(color='#F43F5E', width=3, dash='dash'), marker=dict(size=8)))
        fig_timp_clar.update_layout(title="Extinderea Calendaristică a Termenelor (Luni)", template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_timp_clar, use_container_width=True)

# ---------------- TAB 2: IMPACT RESURSE UMANE ----------------
with tab2:
    st.markdown("<h2 style='color: #F43F5E;'>🔥 Diagnostic Critic: Indicatorul de Burnout Organizațional</h2>", unsafe_allow_html=True)
    
    df_stres_map = df_simulat[['Departament', 'Indice_Stres_Oameni']].copy()
    fig_heatmap = px.density_heatmap(df_stres_map, x="Departament", y="Indice_Stres_Oameni", z="Indice_Stres_Oameni", title="Hartă de Căldură Psihologică: Zonele de Risc și Suprasolicitare", color_continuous_scale=["#1E293B", "#0284C7", "#F43F5E", "#E11D48", "#991B1B"], range_color=[0, 100], template="plotly_dark")
    fig_heatmap.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    if stres_mediu < 35: st.success(f"😊 *Nivel mediu de stres: {stres_mediu:.1f}%* - Resursele lucrează în parametri nominali.")
    elif stres_mediu < 65: st.warning(f"😐 *Nivel mediu de stres: {stres_mediu:.1f}%* - Suprasolicitare moderată.")
    else: st.error(f"🚨 *ALERTĂ COLAPS RESURSE UMANE: {stres_mediu:.1f}%* - Echipele se află în pragul Burnout-ului.")

# ---------------- TAB 3: RECOMANDĂRI DINAMICE NOI ȘI RESTRUCTURATE ----------------
with tab3:
    if solutii_curente["tip_alerta"] == "success":
        st.success(f"### {solutii_curente['titlu']}")
    elif solutii_curente["tip_alerta"] == "info":
        st.info(f"### {solutii_curente['titlu']}")
    elif solutii_curente["tip_alerta"] == "warning":
        st.warning(f"### {solutii_curente['titlu']}")
    else:
        st.error(f"### {solutii_curente['titlu']}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    p1, p2, p3 = st.columns(3)
    
    with p1:
        st.markdown("<div class='sol-card'>", unsafe_allow_html=True)
        st.markdown("#### 🔄 Pilon 1: Metodologie & Agile")
        st.markdown(solutii_curente["agile"])
        st.markdown("</div>", unsafe_allow_html=True)
        
    with p2:
        st.markdown("<div class='sol-card'>", unsafe_allow_html=True)
        st.markdown("#### ⚙️ Pilon 2: Operațional & Tehnic")
        st.markdown(solutii_curente["tech"])
        st.markdown("</div>", unsafe_allow_html=True)
        
    with p3:
        st.markdown("<div class='sol-card'>", unsafe_allow_html=True)
        st.markdown("#### 👥 Pilon 3: Capital Uman (HR)")
        st.markdown(solutii_curente["hr"])
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    
    tip_criza_clean = str(tip_criza).upper()
    text_raport = f"""DOCUMENT MANAGEMENT | NOTĂ OFICIALĂ ADRESATĂ CONSILIULUI DE ADMINISTRAȚIE
De la: Departamentul de Management al Proiectelor (PMO)
Referință: Directivă de Intervenție Strategică de Urgență - Proiect Phoenix

[1. EVALUAREA SITUAȚIEI ȘI STATUS]
Stare curentă detectată: {solutii_curente['titlu'].upper()}
Tip Criză: {tip_criza_clean} | Intensitate Factor Risc: {intensitate_criza:.1f}/3.0

[2. IMPACTUL BRUT ASUPRA TRIPLEI CONSTRÂNGERI]
- Deficit Financiar Net: {depasire_buget:,.2f} EUR
- Întârziere Calendaristică stabilita: {intarziere_luni:.2f} luni
- Indice de Eficiență a Costului (CPI): {cpi:.2f}
- Indice Mediu Stres Personal: {stres_mediu:.1f}%

[3. DIRECTIVE DE INTERVENȚIE APROBATE (AGILE / LEAN / TURNAROUND)]
METODOLOGIE AGILE:
{solutii_curente['agile'].replace('**', '')}

TEHNOLOGIC & OPERAȚIONAL:
{solutii_curente['tech'].replace('**', '')}

CAPITAL UMAN & HR:
{solutii_curente['hr'].replace('**', '')}

Aprobat de: Sistemul Automat de Suport Decizional (IDSDC)
Anul: 2026 | Statut: CONFIDENȚIAL
"""

    st.download_button(
        label="📥 Descarcă Raportul Executiv Actualizat pentru această Criză (.txt)",
        data=text_raport,
        file_name=f"Directiva_Urgenta_{tip_criza_clean}_{intensitate_criza}.txt",
        mime="text/plain",
        type="primary"
    )

# ---------------- TAB 4: GHID METODOLOGIC ----------------
with tab4:
    st.subheader("📘 Fundamentarea Metodologică a Instrumentului IDSDC")
    st.markdown("Acest instrument utilizează ecuațiile liniare de propagare a riscului (Metodologia PMI/PMBOK):")
    st.latex(r"Cost_{Simulat} = Cost_{Initial} \times [1 + (\text{Intensitate} - 1) \times w_{cost}]")
    st.latex(r"Durata_{Simulata} = Durata_{Initial} \times [1 + (\text{Intensitate} - 1) \times w_{timp}]")

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import io
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Tipe Matematikawan",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS WITH IMPROVED COLOR THEORY ---
st.markdown("""
<style>
    /* Import font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main background - Softer gradient */
    .stApp {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%);
        background-attachment: fixed;
    }
    
    /* Title styling - Better readability */
    h1 {
        text-align: center;
        color: #ffffff !important;
        font-size: 3.5em !important;
        font-weight: 900 !important;
        margin-bottom: 10px !important;
        text-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        letter-spacing: -1px;
    }
    
    /* Main container - Cleaner white */
    .main {
        background: #ffffff;
        border-radius: 24px;
        padding: 48px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
        max-width: 900px;
        margin: 40px auto;
    }
    
    /* Question styling - Complementary color */
    .stSubheader {
        font-size: 1.4em !important;
        font-weight: 700 !important;
        color: #1e293b !important;
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        padding: 24px !important;
        border-radius: 16px !important;
        border-left: 6px solid #0ea5e9 !important;
        line-height: 1.6 !important;
        box-shadow: 0 2px 8px rgba(14, 165, 233, 0.1);
    }
    
    /* Radio button styling - Modern cards */
    .stRadio > label {
        background: #f8fafc;
        padding: 16px 20px !important;
        border-radius: 12px !important;
        margin: 10px 0 !important;
        font-weight: 600 !important;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 2px solid #e2e8f0;
        color: #334155 !important;
    }
    
    .stRadio > label:hover {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white !important;
        transform: translateX(8px) scale(1.02);
        border-color: transparent;
        box-shadow: 0 8px 16px rgba(99, 102, 241, 0.3);
    }
    
    /* Button styling - Vibrant but balanced */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        padding: 14px 32px !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 1.05em !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.35) !important;
        letter-spacing: 0.3px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.5) !important;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
    }
    
    .stButton > button:disabled {
        background: #e2e8f0 !important;
        color: #94a3b8 !important;
        box-shadow: none !important;
    }
    
    /* Progress bar - Matching theme */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%) !important;
        border-radius: 10px;
    }
    
    .stProgress > div > div {
        background: #e2e8f0 !important;
        border-radius: 10px;
    }
    
    /* Success message - Harmonious green */
    .stSuccess {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%) !important;
        border-left: 6px solid #10b981 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        color: #064e3b !important;
        font-weight: 600 !important;
    }
    
    /* Header text - Better hierarchy */
    .stMarkdown h3 {
        color: #1e293b !important;
        font-weight: 800 !important;
        margin-bottom: 20px !important;
    }
    
    h2 {
        color: #1e293b !important;
        font-weight: 800 !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Divider - Subtle */
    hr {
        border: 0 !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent) !important;
        margin: 32px 0 !important;
    }
    
    /* Info box - Cohesive colors */
    .stInfo {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%) !important;
        border-left: 6px solid #3b82f6 !important;
        border-radius: 12px !important;
        color: #1e3a8a !important;
    }
    
    /* Score cards enhancement */
    .score-card {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        padding: 28px;
        border-radius: 16px;
        text-align: center;
        border: 2px solid #0ea5e9;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.15);
        transition: transform 0.3s ease;
    }
    
    .score-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(14, 165, 233, 0.25);
    }
    
    .score-label {
        color: #475569;
        font-size: 0.85em;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }
    
    .score-value {
        font-size: 3em;
        font-weight: 900;
        background: linear-gradient(135deg, #6366f1, #8b5cf6, #d946ef);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
</style>
""", unsafe_allow_html=True)

# --- 1. TENTUKAN KUIS ANDA ---

OPTIONS = {
    "Setuju Banget": 2,
    "Setuju": 1,
    "Biasa Aja / Netral": 0,
    "Nggak Setuju": -1,
    "Nggak Setuju Banget": -2
}

QUESTIONS = [
    {
        "question": "Matematika itu paling keren pas bisa dipakai buat mecahin masalah di dunia nyata.",
        "weights": {'x': 1, 'y': 0}
    },
    {
        "question": "Aku suka banget sama struktur abstrak, biarpun nggak tahu bakal dipakai buat apa.",
        "weights": {'x': -1, 'y': 0}
    },
    {
        "question": "Aku seringnya 'ngeh' duluan solusinya apa, baru deh mikirin bukti formalnya.",
        "weights": {'x': 0, 'y': 1}
    },
    {
        "question": "Aku nggak bakal percaya suatu hasil sebelum ngecek satu per satu langkah logis dan definisinya.",
        "weights": {'x': 0, 'y': -1}
    },
    {
        "question": "Aku lebih tertarik ngembangin aplikasi praktis daripada eksplorasi teori murni.",
        "weights": {'x': 1, 'y': 0}
    },
    {
        "question": "Gambar diagram atau corat-coret bentuk geometri itu penting banget buat aku biar paham konsep yang susah.",
        "weights": {'x': 0, 'y': 1}
    },
    {
        "question": "Aku menikmati banget proses nyusun bukti dari awal (aksioma), selangkah demi selangkah.",
        "weights": {'x': 0, 'y': -1}
    },
    {
        "question": "Keindahan matematika murni lebih penting daripada aplikasi praktisnya.",
        "weights": {'x': -1, 'y': 0}
    },
    {
        "question": "Aku lebih suka coding dan simulasi daripada menulis bukti manual di kertas.",
        "weights": {'x': 1, 'y': 0}
    },
    {
        "question": "Intuisi dan visualisasi lebih membantu aku daripada definisi formal yang kaku.",
        "weights": {'x': 0, 'y': 1}
    },
    {
        "question": "Aku selalu mulai dari definisi presisi dan aksioma sebelum eksplorasi ide.",
        "weights": {'x': 0, 'y': -1}
    },
    {
        "question": "Matematika yang berguna di engineering atau sains lebih menarik bagiku.",
        "weights": {'x': 1, 'y': 0}
    }
]

# --- 2. HITUNG SKOR MAKSIMUM ---

max_x = 0
max_y = 0
for q in QUESTIONS:
    max_x += abs(q['weights']['x'] * 2) 
    max_y += abs(q['weights']['y'] * 2)

plot_limit = max(max_x, max_y) + 2

# --- 3. INITIALIZE SESSION STATE ---

if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
    st.session_state.answers = {}

# --- 4. BUILD STREAMLIT APP ---

st.title("🧮 Cek Tipe Matematikawan Lo!")
st.markdown(
    "<div style='text-align: center; color: #f8fafc; font-size: 1.15em; margin-bottom: 30px; font-weight: 500;'>"
    "Lo tipe <b>'visioner'</b> yang liat gambaran gede atau <b>'arsitek'</b> yang super teliti? "
    "Suka teori abstrak atau model yang nyata? Kuis seru ini bakal bantu lo nemuin tipe matematikawan lo! 🎯"
    "</div>",
    unsafe_allow_html=True
)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# Progress section with better styling
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    progress = (st.session_state.current_question) / len(QUESTIONS)
    st.progress(min(progress, 0.99))
    st.markdown(
        f"<div style='text-align: center; font-weight: 700; color: #1e293b; font-size: 1.1em; margin-top: 12px;'>"
        f"Soal {st.session_state.current_question + 1} dari {len(QUESTIONS)}"
        f"</div>",
        unsafe_allow_html=True
    )

st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

if st.session_state.current_question < len(QUESTIONS):
    current_q = QUESTIONS[st.session_state.current_question]

    st.subheader(current_q["question"])
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # Get previous answer if exists, otherwise default to "Biasa Aja / Netral"
    default_index = 2
    if st.session_state.current_question in st.session_state.answers:
        prev_answer = st.session_state.answers[st.session_state.current_question]
        default_index = list(OPTIONS.keys()).index(prev_answer)
    
    answer = st.radio(
        "Pilih jawaban lo:",
        options=OPTIONS.keys(),
        index=default_index,
        key=f"radio_{st.session_state.current_question}",
        label_visibility="collapsed"
    )
    
    # Always save the current answer to session state
    st.session_state.answers[st.session_state.current_question] = answer

    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("← Sebelumnya", disabled=(st.session_state.current_question == 0), use_container_width=True):
            st.session_state.current_question -= 1
            st.rerun()

    with col3:
        if st.session_state.current_question < len(QUESTIONS) - 1:
            if st.button("Berikutnya →", use_container_width=True):
                st.session_state.current_question += 1
                st.rerun()
        else:
            if st.button("✨ Lihat Hasil Gue!", use_container_width=True):
                st.session_state.current_question = len(QUESTIONS)
                st.rerun()

# --- 5. PROSES HASIL ---

if st.session_state.current_question == len(QUESTIONS):
    st.markdown("---")
    
    score_x = 0
    score_y = 0

    for i, q in enumerate(QUESTIONS):
        answer_text = st.session_state.answers[i]
        answer_score = OPTIONS[answer_text]
        
        score_x += answer_score * q['weights']['x']
        score_y += answer_score * q['weights']['y']

    # Score display with enhanced styling
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"<div class='score-card'>"
            f"<div class='score-label'>Skor X: Murni ↔ Terapan</div>"
            f"<div class='score-value'>{score_x}</div>"
            f"</div>",
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"<div class='score-card'>"
            f"<div class='score-label'>Skor Y: Formalis ↔ Intuitif</div>"
            f"<div class='score-value'>{score_y}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

    # --- 6. PLOT SPEKTRUM ---
    
    fig, ax = plt.subplots(figsize=(11, 11), facecolor='white')
    fig.patch.set_alpha(0.0)
    
    ax.set_xlim(-plot_limit, plot_limit)
    ax.set_ylim(-plot_limit, plot_limit)
    
    ax.grid(True, linestyle='--', alpha=0.2, linewidth=0.8, zorder=0)
    ax.axhline(0, color='#64748b', linewidth=2.5, zorder=1, alpha=0.5)
    ax.axvline(0, color='#64748b', linewidth=2.5, zorder=1, alpha=0.5)
    
    # Quadrant colors with better color theory
    ax.fill_between([-plot_limit, 0], 0, plot_limit, color='#818cf8', alpha=0.12, zorder=1)
    ax.text(-plot_limit/2, plot_limit/2, "Si Visioner\n(Murni / Intuitif)", ha='center', va='center', fontsize=14, alpha=0.75, fontweight='bold', color='#4338ca')
    
    ax.fill_between([0, plot_limit], 0, plot_limit, color='#f472b6', alpha=0.12, zorder=1)
    ax.text(plot_limit/2, plot_limit/2, "Si Pemodel\n(Terapan / Intuitif)", ha='center', va='center', fontsize=14, alpha=0.75, fontweight='bold', color='#be185d')
    
    ax.fill_between([-plot_limit, 0], -plot_limit, 0, color='#a78bfa', alpha=0.12, zorder=1)
    ax.text(-plot_limit/2, -plot_limit/2, "Si Arsitek\n(Murni / Formalis)", ha='center', va='center', fontsize=14, alpha=0.75, fontweight='bold', color='#6d28d9')
    
    ax.fill_between([0, plot_limit], -plot_limit, 0, color='#2dd4bf', alpha=0.12, zorder=1)
    ax.text(plot_limit/2, -plot_limit/2, "Si Analis\n(Terapan / Formalis)", ha='center', va='center', fontsize=14, alpha=0.75, fontweight='bold', color='#0f766e')

    # Axis labels
    ax.text(0, plot_limit+0.7, "✨ INTUITIF (Feeling)", ha='center', va='bottom', fontsize=14, fontweight='bold', color='#475569')
    ax.text(0, -plot_limit-0.7, "🧬 FORMALIS (Logika)", ha='center', va='top', fontsize=14, fontweight='bold', color='#475569')
    ax.text(plot_limit+0.7, 0, "⚙️ TERAPAN", ha='right', va='center', fontsize=14, fontweight='bold', color='#475569', rotation=270)
    ax.text(-plot_limit-0.7, 0, "🎨 MURNI", ha='left', va='center', fontsize=14, fontweight='bold', color='#475569', rotation=90)

    # User position marker
    ax.plot(score_x, score_y, 'o', markersize=26, color='#fbbf24', markeredgecolor='#6366f1', markeredgewidth=4, zorder=3, alpha=0.95)
    ax.text(score_x, score_y-1.8, "LO DI SINI", ha='center', va='center', fontsize=12, fontweight='bold', color='#1e293b', 
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='#6366f1', linewidth=2))

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    ax.set_xticks([])
    ax.set_yticks([])

    st.pyplot(fig, use_container_width=True)

    # --- 7. PERSONALITY DESCRIPTION ---
    
    st.markdown("---")
    st.markdown("<h3 style='text-align: center; margin-bottom: 30px;'>🎯 Tipe Matematikawan Lo Adalah:</h3>", unsafe_allow_html=True)

    if score_x < 0:
        if score_y > 0:
            st.markdown(
                "<div style='background: linear-gradient(135deg, #818cf8, #6366f1); padding: 36px; border-radius: 20px; color: white; box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);'>"
                "<h2 style='color: white; text-align: center; margin-top: 0; margin-bottom: 20px;'>✨ Si Visioner (Murni / Intuitif)</h2>"
                "<p style='font-size: 1.15em; line-height: 1.9;'>"
                "Lo tertarik sama 'gambaran besar' di matematika abstrak. Lo mungkin mikirnya pake bentuk, struktur, dan hubungan. "
                "Lo bisa jadi 'ngeliat' jawaban dari masalah jauh sebelum bukti formalnya kelar. "
                "Lo cocok gaul sama ahli geometri dan topologi yang suka menjelajahi dunia pemikiran baru."
                "</p></div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<div style='background: linear-gradient(135deg, #a78bfa, #8b5cf6); padding: 36px; border-radius: 20px; color: white; box-shadow: 0 10px 30px rgba(139, 92, 246, 0.3);'>"
                "<h2 style='color: white; text-align: center; margin-top: 0; margin-bottom: 20px;'>🏗️ Si Arsitek (Murni / Formalis)</h2>"
                "<p style='font-size: 1.15em; line-height: 1.9;'>"
                "Lo itu tipe 'pembangun'. Lo percaya matematika itu kayak bangunan logis yang megah, dibangun dari nol, mulai dari aksioma dan definisi. "
                "Lo ngerasa keren aja gitu liat bukti yang presisi dan pas. "
                "Lo cocok gaul sama ahli logika dan aljabar yang mastiin fondasi matematika itu kokoh."
                "</p></div>",
                unsafe_allow_html=True
            )
    else:
        if score_y > 0:
            st.markdown(
                "<div style='background: linear-gradient(135deg, #f472b6, #ec4899); padding: 36px; border-radius: 20px; color: white; box-shadow: 0 10px 30px rgba(236, 72, 153, 0.3);'>"
                "<h2 style='color: white; text-align: center; margin-top: 0; margin-bottom: 20px;'>🎨 Si Pemodel (Terapan / Intuitif)</h2>"
                "<p style='font-size: 1.15em; line-height: 1.9;'>"
                "Intuisi lo kuat banget buat ngertiin sistem di dunia nyata. Lo bisa liat masalah rumit (di fisika, biologi, atau keuangan) dan "
                "langsung 'ngeh' pola matematika di baliknya. Lo jago bikin model simpel yang nangkep inti masalahnya, "
                "biarpun bagian detailnya lo serahin ke orang lain. Lo itu pemecah masalah 'gambaran besar'."
                "</p></div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<div style='background: linear-gradient(135deg, #2dd4bf, #14b8a6); padding: 36px; border-radius: 20px; color: white; box-shadow: 0 10px 30px rgba(20, 184, 166, 0.3);'>"
                "<h2 style='color: white; text-align: center; margin-top: 0; margin-bottom: 20px;'>⚙️ Si Analis (Terapan / Formalis)</h2>"
                "<p style='font-size: 1.15em; line-height: 1.9;'>"
                "Lo itu jagonya detail. Lo tau 'kira-kira' aja nggak cukup kalo udah urusan aplikasi di dunia nyata. "
                "Lo jago di analisis numerik, statistik, dan optimisasi, mastiin model itu nggak cuma jalan, tapi juga akurat, stabil, dan bisa diandelin. "
                "Lo cocok gaul sama para 'quant' dan insinyur yang bikin dunia modern ini jalan."
                "</p></div>",
                unsafe_allow_html=True
            )

    st.markdown("---")
    
    # --- 8. MATEMATIKAWAN TERKENAL & CABANG MATEMATIKA ---
    
    st.markdown("<h3 style='text-align: center; margin-bottom: 30px; margin-top: 40px;'>👥 Matematikawan Terkenal yang Cocok dengan Lo</h3>", unsafe_allow_html=True)
    
    # Define famous mathematicians for each type
    mathematicians = {
        "visioner": [
            {"name": "Bernhard Riemann", "desc": "Ahli geometri yang visioner, menciptakan konsep geometri non-Euclidean yang mengubah pemahaman ruang", "era": "1826-1866"},
            {"name": "Henri Poincaré", "desc": "Polymath yang intuitif, pelopor topologi dan teori chaos dengan intuisi geometri yang luar biasa", "era": "1854-1912"},
            {"name": "Srinivasa Ramanujan", "desc": "Genius intuitif yang menemukan formula kompleks lewat intuisi murni tanpa bukti formal", "era": "1887-1920"}
        ],
        "arsitek": [
            {"name": "David Hilbert", "desc": "Arsitek sistem aksioma modern, menetapkan fondasi matematika dengan 23 masalah terkenalnya", "era": "1862-1943"},
            {"name": "Emmy Noether", "desc": "Pembangun teori aljabar abstrak dengan pendekatan sistematis dan formal yang elegan", "era": "1882-1935"},
            {"name": "André Weil", "desc": "Arsitek teori bilangan modern dengan pendekatan formal dan struktural yang sangat presisi", "era": "1906-1998"}
        ],
        "pemodel": [
            {"name": "Isaac Newton", "desc": "Pelopor kalkulus untuk memecahkan masalah fisika dunia nyata, intuitif tapi aplikatif", "era": "1643-1727"},
            {"name": "Leonhard Euler", "desc": "Master problem-solver yang aplikatif, menyelesaikan ribuan masalah praktis dengan intuisi kuat", "era": "1707-1783"},
            {"name": "John von Neumann", "desc": "Visioner terapan di teori game, komputasi, dan fisika kuantum dengan intuisi luar biasa", "era": "1903-1957"}
        ],
        "analis": [
            {"name": "Carl Friedrich Gauss", "desc": "Pangeran matematika dengan ketepatan komputasi legendaris dan analisis yang sempurna", "era": "1777-1855"},
            {"name": "Pierre-Simon Laplace", "desc": "Master analisis matematika terapan di astronomi dan probabilitas dengan presisi tinggi", "era": "1749-1827"},
            {"name": "John Tukey", "desc": "Pelopor statistik modern dan analisis data, menciptakan metode praktis yang presisi", "era": "1915-2000"}
        ]
    }
    
    # Determine personality type
    if score_x < 0:
        if score_y > 0:
            personality_key = "visioner"
        else:
            personality_key = "arsitek"
    else:
        if score_y > 0:
            personality_key = "pemodel"
        else:
            personality_key = "analis"
    
    # Display mathematicians
    cols = st.columns(3)
    for idx, math in enumerate(mathematicians[personality_key]):
        with cols[idx]:
            st.markdown(
                f"<div style='background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); padding: 24px; border-radius: 16px; "
                f"border: 2px solid #e2e8f0; height: 100%; box-shadow: 0 2px 8px rgba(0,0,0,0.05);'>"
                f"<h4 style='color: #6366f1; margin-top: 0; font-size: 1.3em;'>{math['name']}</h4>"
                f"<p style='color: #64748b; font-size: 0.85em; font-weight: 600; margin-bottom: 12px;'>{math['era']}</p>"
                f"<p style='color: #475569; line-height: 1.6; font-size: 0.95em;'>{math['desc']}</p>"
                f"</div>",
                unsafe_allow_html=True
            )
    
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    
    # --- 9. CABANG MATEMATIKA YANG MENARIK ---
    
    st.markdown("<h3 style='text-align: center; margin-bottom: 30px;'>📚 Cabang Matematika yang Menarik Buat Lo</h3>", unsafe_allow_html=True)
    
    # Define mathematical fields for each type
    math_fields = {
        "visioner": [
            {
                "name": "🌀 Topologi", 
                "desc": "Studi tentang bentuk dan ruang yang bertransformasi. Lo bakal suka konsep abstrak seperti manifold, homotopi, dan ruang-ruang eksotis.",
                "topics": "Topologi Aljabar • Teori Simpul • Manifold"
            },
            {
                "name": "🎨 Geometri Diferensial", 
                "desc": "Geometri di permukaan melengkung dengan kalkulus. Perfect buat yang suka visualisasi dan intuisi geometris yang kuat.",
                "topics": "Kurva & Permukaan • Tensor • Geometri Riemann"
            },
            {
                "name": "🔮 Teori Kategori", 
                "desc": "Bahasa abstrak yang menyatukan berbagai cabang matematika. Lo bakal suka pola universal dan struktur di balik struktur.",
                "topics": "Functor • Natural Transformation • Category Theory"
            },
            {
                "name": "🌌 Geometri Aljabar", 
                "desc": "Studi bentuk geometri lewat persamaan aljabar. Kombinasi indah antara visualisasi geometris dan struktur aljabar abstrak.",
                "topics": "Varieties • Schemes • Cohomology Theory"
            },
            {
                "name": "🎭 Teori Representasi", 
                "desc": "Cara melihat struktur abstrak lewat transformasi linear. Menghubungkan aljabar dengan geometri secara intuitif.",
                "topics": "Group Representations • Lie Groups • Character Theory"
            },
            {
                "name": "🔄 Sistem Dinamik", 
                "desc": "Studi pola perubahan dan chaos di sistem yang evolving. Visualisasi fractal dan attractor yang memukau.",
                "topics": "Chaos Theory • Fractals • Bifurcation Theory"
            }
        ],
        "arsitek": [
            {
                "name": "🏛️ Teori Himpunan & Logika", 
                "desc": "Fondasi dari semua matematika. Lo bakal menikmati membangun matematika dari aksioma dasar dengan presisi sempurna.",
                "topics": "Aksioma ZFC • Model Theory • Proof Theory"
            },
            {
                "name": "🔢 Aljabar Abstrak", 
                "desc": "Studi struktur aljabar murni seperti grup, ring, dan field. Sistematis, elegan, dan beautifully structured.",
                "topics": "Group Theory • Ring Theory • Galois Theory"
            },
            {
                "name": "📐 Teori Bilangan", 
                "desc": "Eksplorasi mendalam sifat bilangan bulat dengan bukti yang rigorous dan elegant. The queen of mathematics.",
                "topics": "Number Theory • Diophantine Equations • Modular Forms"
            },
            {
                "name": "🧩 Kombinatorika", 
                "desc": "Seni menghitung dan menyusun objek diskrit dengan metode yang presisi. Struktur yang elegant dan proof yang beautiful.",
                "topics": "Graph Theory • Enumerative Combinatorics • Design Theory"
            },
            {
                "name": "🔐 Kriptografi & Teori Coding", 
                "desc": "Matematika di balik keamanan data dan komunikasi. Membutuhkan pemahaman formal yang sangat presisi.",
                "topics": "Public Key Cryptography • Error Correcting Codes • Lattice Theory"
            },
            {
                "name": "⚖️ Teori Ukuran & Integrasi", 
                "desc": "Fondasi rigorous dari kalkulus modern. Membangun konsep integral dan probabilitas dari ground up.",
                "topics": "Measure Theory • Lebesgue Integration • Ergodic Theory"
            }
        ],
        "pemodel": [
            {
                "name": "🌊 Persamaan Diferensial", 
                "desc": "Model perubahan di dunia nyata - dari cuaca, populasi, hingga aliran fluida. Powerful dan sangat aplikatif.",
                "topics": "PDE • Dynamical Systems • Chaos Theory"
            },
            {
                "name": "🎲 Probabilitas & Stokastik", 
                "desc": "Matematika ketidakpastian untuk finance, machine learning, dan sistem kompleks. Intuitive dan practical.",
                "topics": "Stochastic Calculus • Random Processes • Markov Chains"
            },
            {
                "name": "🤖 Matematika Komputasi", 
                "desc": "Kombinasi matematika dan algoritma untuk AI, data science, dan optimization. Super relevant di era digital.",
                "topics": "Machine Learning • Graph Theory • Optimization"
            },
            {
                "name": "🎯 Riset Operasi", 
                "desc": "Optimasi keputusan di sistem kompleks - supply chain, scheduling, resource allocation. Langsung applicable ke bisnis.",
                "topics": "Linear Programming • Integer Programming • Network Optimization"
            },
            {
                "name": "🎮 Teori Game & Keputusan", 
                "desc": "Analisis strategi dalam situasi kompetitif dan kooperatif. Aplikasi di ekonomi, politik, dan AI.",
                "topics": "Game Theory • Decision Theory • Auction Theory"
            },
            {
                "name": "🧬 Matematika Biologi", 
                "desc": "Model matematis untuk sistem biologis - epidemi, ekologi, genetika. Interdisciplinary dan impact-driven.",
                "topics": "Population Dynamics • Epidemiology • Systems Biology"
            },
            {
                "name": "🌐 Teori Jaringan & Graf", 
                "desc": "Analisis struktur koneksi di social networks, internet, dan sistem kompleks. Very relevant untuk data science.",
                "topics": "Network Science • Social Networks • Community Detection"
            }
        ],
        "analis": [
            {
                "name": "📊 Analisis Numerik", 
                "desc": "Metode presisi tinggi untuk menyelesaikan masalah matematika di komputer. Essential untuk engineering dan science.",
                "topics": "Numerical Methods • Finite Elements • Error Analysis"
            },
            {
                "name": "📈 Analisis Real & Kompleks", 
                "desc": "Studi mendalam tentang fungsi, limit, dan kontinuitas dengan rigorous proofs. Foundation of calculus.",
                "topics": "Real Analysis • Complex Analysis • Functional Analysis"
            },
            {
                "name": "💹 Matematika Keuangan", 
                "desc": "Aplikasi matematika presisi untuk pricing, risk management, dan trading strategies di financial markets.",
                "topics": "Quantitative Finance • Options Pricing • Risk Models"
            },
            {
                "name": "📉 Optimasi & Kontrol", 
                "desc": "Mencari solusi terbaik dengan constraints ketat. Critical untuk engineering, manufacturing, dan logistics.",
                "topics": "Convex Optimization • Optimal Control • Calculus of Variations"
            },
            {
                "name": "📡 Pemrosesan Sinyal", 
                "desc": "Analisis dan transformasi data temporal/spatial. Fundamental untuk audio, image processing, dan communications.",
                "topics": "Fourier Analysis • Wavelets • Digital Signal Processing"
            },
            {
                "name": "🔬 Statistika & Analisis Data", 
                "desc": "Ekstraksi insight dari data dengan metode yang rigorous. Essential di era big data dan AI.",
                "topics": "Statistical Inference • Regression Analysis • Bayesian Statistics"
            },
            {
                "name": "⚙️ Matematika Teknik", 
                "desc": "Tools matematis untuk mechanical, electrical, dan civil engineering. Precision-oriented dan highly applicable.",
                "topics": "Laplace Transforms • Partial Differential Equations • Finite Element Analysis"
            },
            {
                "name": "🎲 Aktuaria & Manajemen Risiko", 
                "desc": "Quantifikasi dan mitigasi risiko finansial dengan analisis statistik yang presisi. High-demand career path.",
                "topics": "Life Contingencies • Loss Models • Credibility Theory"
            }
        ]
    }
    
    # Display mathematical fields
    for field in math_fields[personality_key]:
        st.markdown(
            f"<div style='background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%); padding: 28px; border-radius: 16px; "
            f"margin-bottom: 20px; border-left: 6px solid #6366f1; box-shadow: 0 4px 12px rgba(99,102,241,0.1);'>"
            f"<h4 style='color: #1e293b; margin-top: 0; font-size: 1.4em; margin-bottom: 12px;'>{field['name']}</h4>"
            f"<p style='color: #475569; line-height: 1.7; font-size: 1.05em; margin-bottom: 16px;'>{field['desc']}</p>"
            f"<div style='background: #f0f9ff; padding: 12px 16px; border-radius: 8px; border-left: 3px solid #0ea5e9;'>"
            f"<p style='color: #0c4a6e; margin: 0; font-size: 0.9em; font-weight: 600;'>📌 {field['topics']}</p>"
            f"</div>"
            f"</div>",
            unsafe_allow_html=True
        )
    
    st.markdown("---")
    
    # --- 10. SAVE RESULTS (Auto-save to CSV) ---
    
    result_data = {
        "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Skor_X_Murni_Terapan": [score_x],
        "Skor_Y_Formalis_Intuitif": [score_y],
    }
    
    for i, q in enumerate(QUESTIONS):
        result_data[f"Soal_{i+1}"] = [st.session_state.answers[i]]
    
    if score_x < 0:
        if score_y > 0:
            personality = "Si Visioner (Murni / Intuitif)"
        else:
            personality = "Si Arsitek (Murni / Formalis)"
    else:
        if score_y > 0:
            personality = "Si Pemodel (Terapan / Intuitif)"
        else:
            personality = "Si Analis (Terapan / Formalis)"
    
    result_data["Tipe_Matematikawan"] = [personality]
    
    df_result = pd.DataFrame(result_data)
    
    try:
        existing_df = pd.read_csv("kuis_responses.csv")
        updated_df = pd.concat([existing_df, df_result], ignore_index=True)
        updated_df.to_csv("kuis_responses.csv", index=False, encoding='utf-8-sig')
    except FileNotFoundError:
        df_result.to_csv("kuis_responses.csv", index=False, encoding='utf-8-sig')
    
    st.success("✅ Hasil kuis lo udah tersimpan!")
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 Ulang Kuis", use_container_width=True):
            st.session_state.current_question = 0
            st.session_state.answers = {}
            st.rerun()

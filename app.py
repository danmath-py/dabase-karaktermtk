import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import io
import gspread
from google.oauth2.service_account import Credentials

# --- 1. PAGE CONFIG & CSS ---
st.set_page_config(
    page_title="Database Karakteristik Matematika",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

APP_VERSION = "v1.1 - Fixed UI"

def load_css():
    """Loads all custom CSS into the app."""
    st.markdown("""
    <style>
        /* Import font */
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;600;700;800;900&display=swap&v=1'); /* <-- URL Noto Sans */
        
        * {
            font-family: 'Noto Sans', sans-serif; /* <-- Nama Font Noto Sans */
        }
        
        .stApp {
            background: linear-gradient(to right, #881919, #761b1a);
            background-attachment: fixed;
        }
        
        /* REVISI BANNER: Hilangkan padding atas dari block container bawaan */
        .block-container {
            padding-top: 2rem !important;  
        }
        
        /* REVISI BANNER: Pastikan gambar banner menyentuh tepi */
        .stImage > img {
            width: 100%;
        }
        
        .main-container {
            background: #ffffff;
            border-radius: 24px;
            padding: 0px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
            max-width: 900px;
            margin: 40px auto;
        }
        
        /* REVISI BOX PUTIH: Title kembali ke dalam box putih */
        h1 {
            text-align: center;
            color: #ffffff !important; /* Warna gelap */
            font-size: 3.5em !important;
            font-weight: 900 !important;
            margin-top: 0 !important; /* Hapus margin atas */
            margin-bottom: 10px !important;
            text-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            letter-spacing: -1px;
        }

        /* REVISI BOX PUTIH: Subtitle kembali ke dalam box putih */
        .stMarkdown > div[style*="text-align: center; color: #f8f9fa;"] {
            font-size: 1.15em;
            font-weight: 500;
            margin: 0 auto 30px auto;
        }
        
        /* Question styling */
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
        
        /* Radio button styling */
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

        /* Text Input */
        .stTextInput > div > div > input {
            background: #f8fafc;
            border: 2px solid #e2e8f0;
            border-radius: 12px !important;
            padding: 24px 20px !important;
            font-size: 1.1em !important;
            font-weight: 600 !important;
            color: #334155 !important;
            transition: all 0.3s ease;
        }
        .stTextInput > div > div > input:focus {
            border-color: #6366f1;
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2);
        }
        
        /* Text Area */
        .stTextArea > div > textarea {
            background: #f8fafc;
            border: 2px solid #e2e8f0;
            border-radius: 12px !important;
            padding: 16px 20px !important;
            font-size: 1.1em !important;
            font-weight: 600 !important;
            color: #334155 !important;
            transition: all 0.3s ease;
            min-height: 120px;
        }
        .stTextArea > div > textarea:focus {
            border-color: #6366f1;
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2);
        }

        /* Selectbox (Dropdown) - STYLING UNTUK MATKUL */
        .stSelectbox > div > div {
            background: #f8fafc;
            border: 2px solid #e2e8f0;
            border-radius: 12px !important;
            padding: 8px 12px !important;
            font-size: 1.1em !important;
            font-weight: 600 !important;
            color: #334155 !important;
            transition: all 0.3s ease;
        }
        .stSelectbox > div > div:focus-within {
            border-color: #6366f1;
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2);
        }
        
        /* Multiselect */
        .stMultiSelect > div > div {
            background: #f8fafc;
            border: 2px solid #e2e8f0;
            border-radius: 12px !important;
            padding: 8px 12px !important;
            font-weight: 600 !important;
            color: #334155 !important;
            transition: all 0.3s ease;
        }
        .stMultiSelect > div > div:focus-within {
            border-color: #6366f1;
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2);
        }
        
        /* Button styling */
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
            cursor: not-allowed !important;
        }
        
        /* Progress bar */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%) !important;
            border-radius: 10px;
        }
        
        .stProgress > div > div {
            background: #e2e8f0 !important;
            border-radius: 10px;
        }
        
        /* Success message */
        .stSuccess {
            background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%) !important;
            border-left: 6px solid #10b981 !important;
            border-radius: 12px !important;
            padding: 20px !important;
            color: #064e3b !important;
            font-weight: 600 !important;
        }

        /* Error message (for validation) */
        .stError {
            background: linear-gradient(135deg, #ffe4e6 0%, #fecdd3 100%) !important;
            border-left: 6px solid #f43f5e !important;
            border-radius: 12px !important;
            color: #881337 !important;
        }
        
        /* Header text */
        .stMarkdown h3 {
            color: #f8f9fa !important;
            font-weight: 800 !important;
            margin-bottom: 20px !important;
        }
        
        /* Section Headers */
        h2 {
            color: #f8f9fa !important;
            font-weight: 800 !important;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            border-bottom: 3px solid #6366f1;
            padding-bottom: 10px;
        }
        
        /* Divider */
        hr {
            border: 0 !important;
            height: 2px !important;
            background: linear-gradient(90deg, transparent, #e2e8f0, transparent) !important;
            margin: 32px 0 !important;
        }
        
        /* Info box */
        .stInfo {
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%) !important;
            border-left: 6px solid #3b82f6 !important;
            border-radius: 12px !important;
            color: #1e3a8a !important;
        }
        
        /* Score cards */
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


# --- 2. SURVEY & QUIZ CONSTANTS ---

PERSONALITY_OPTIONS = {
    "Setuju Banget": 2,
    "Setuju": 1,
    "Nggak Setuju": -1,
    "Nggak Setuju Banget": -2
}

PERSONALITY_QUESTIONS = [
    {
        "question": "Matematika itu paling keren pas bisa dipakai buat mecahin masalah di dunia nyata.",
        "weights": {'x': 1.5, 'y': 0}
    },
    {
        "question": "Aku suka banget sama struktur abstrak, biarpun nggak tahu bakal dipakai buat apa.",
        "weights": {'x': -1, 'y': 0}
    },
    {
        "question": "Aku seringnya 'ngeh' duluan solusinya apa, baru deh mikirin bukti formalnya.",
        "weights": {'x': 0, 'y': 1.7}
    },
    {
        "question": "Aku nggak bakal percaya suatu hasil sebelum ngecek satu per satu langkah logis dan definisinya.",
        "weights": {'x': 0, 'y': -1.4}
    },
    {
        "question": "Aku lebih tertarik ngembangin aplikasi praktis daripada eksplorasi teori matematika murni.",
        "weights": {'x': 1.1, 'y': 0}
    },
    {
        "question": "Gambar diagram atau corat-coret bentuk geometri itu penting banget buat aku biar paham konsep yang susah.",
        "weights": {'x': 0, 'y': 0.8}
    },
    {
        "question": "Aku menikmati banget proses nyusun bukti dari awal (aksioma), selangkah demi selangkah.",
        "weights": {'x': 0, 'y': -0.5}
    },
    {
        "question": "Keindahan matematika murni bisa lebih menarik daripada aplikasi praktisnya.",
        "weights": {'x': -0.7, 'y': 0}
    },
    {
        "question": "Aku lebih suka coding dan simulasi daripada menulis bukti manual di kertas.",
        "weights": {'x': 0.8, 'y': 0}
    },
    {
        "question": "Intuisi dan visualisasi lebih membantu aku daripada definisi formal yang kaku.",
        "weights": {'x': 0, 'y': 0.6}
    },
    {
        "question": "Aku selalu mulai dari definisi presisi dan aksioma sebelum eksplorasi ide.",
        "weights": {'x': 0, 'y': -1.8}
    },
    {
        "question": "Matematika yang berguna di engineering atau sains lebih menarik bagiku.",
        "weights": {'x': 2, 'y': 0}
    },
    {
        "question": "Mencari nilai prima terbesar yang dapat dihitung saat ini keren! Walau gatau sih dipake buat apa",
        "weights": {'x': -0.6, 'y': 0}  
    },
    {
        "question": "Lebih gampang membayangkan partisi di matematika diskret seperti bagian dari kue dibandingkan membaca definisi formalnya",
        "weights": {'x': 0, 'y': 1.9}   
    },
    {
        "question": "Gw gasuka jawaban soal yang ga jelas alur penyelesaiannya dari mana ke mana",
        "weights": {'x': 0, 'y': 0.5}
    }
]

MASTER_SURVEY_QUESTIONS = [
    # SECTION: GENERAL
    {"id": "nama", "section": "GENERAL", "text": "Nama Lengkap", "type": "text_input", "required": True},
    {"id": "nim", "section": "GENERAL", "text": "NIM", "type": "text_input", "required": True},
    {"id": "provinsi", "section": "GENERAL", "text": "Asal Provinsi", "type": "text_input", "required": True},
    {"id": "kab_kota", "section": "GENERAL", "text": "Asal Kabupaten/Kota", "type": "text_input", "required": True},
    {"id": "whatsapp", "section": "GENERAL", "text": "Nomor WhatsApp (Format: wa.me/62...)", "type": "text_input", "required": True},
    {"id": "beasiswa", "section": "GENERAL", "text": "Apakah Kamu Penerima Beasiswa?", "type": "radio", "options": ["Ya", "Tidak"], "required": True},
    {"id": "daerah_tinggal", "section": "GENERAL", "text": "Daerah tempat tinggal?", "type": "radio", "options": ["Babakan Raya", "Babakan Tengah", "Babakan Lebak", "Babakan Lio", "Perwira", "Dramaga Cantik", "Cibanteng", "Lainnya"], "required": True},  
    {"id": "status_tinggal", "section": "GENERAL", "text": "Status tempat tinggal?", "type": "radio", "options": ["Kost", "Asrama", "Kontrakan", "Apartkos", "Rumah keluarga", "Lainnya"], "required": True},  
    
    # SECTION: TIPE MATEMATIKA PART I
    {"id": "tipe_1", "section": "TIPE MATEMATIKA PART I", "text": PERSONALITY_QUESTIONS[0]["question"], "type": "personality_quiz", "personality_q_index": 0, "required": True},
    {"id": "tipe_2", "section": "TIPE MATEMATIKA PART I", "text": PERSONALITY_QUESTIONS[1]["question"], "type": "personality_quiz", "personality_q_index": 1, "required": True},
    {"id": "tipe_3", "section": "TIPE MATEMATIKA PART I", "text": PERSONALITY_QUESTIONS[2]["question"], "type": "personality_quiz", "personality_q_index": 2, "required": True},
    {"id": "tipe_4", "section": "TIPE MATEMATIKA PART I", "text": PERSONALITY_QUESTIONS[3]["question"], "type": "personality_quiz", "personality_q_index": 3, "required": True},
    {"id": "tipe_5", "section": "TIPE MATEMATIKA PART I", "text": PERSONALITY_QUESTIONS[4]["question"], "type": "personality_quiz", "personality_q_index": 4, "required": True},
    
    # SECTION: MASUK KE PRODI MATEMATIKA
    {"id": "jalur_masuk", "section": "MASUK KE PRODI MATEMATIKA", "text": "Jalur Masuk", "type": "radio", "options": ["SNBP", "SNBT", "Mandiri", "Jaketos", "BUD", "PIN", "Lainnya"], "required": True},  
    {"id": "pilihan_ke", "section": "MASUK KE PRODI MATEMATIKA", "text": "Pilihan ke Berapa", "type": "radio", "options": ["1", "2"], "required": True},
    {"id": "alasan_ipb", "section": "MASUK KE PRODI MATEMATIKA", "text": "Alasan Masuk IPB", "type": "text_area", "required": True},
    {"id": "alasan_prodi", "section": "MASUK KE PRODI MATEMATIKA", "text": "Alasan Masuk Prodi Matematika", "type": "text_area", "required": True},
    {"id": "info_prodi", "section": "MASUK KE PRODI MATEMATIKA", "text": "Dari mana kamu pertama kali mengetahui informasi tentang prodi Matematika IPB?", "type": "radio", "options": ["Sosmed", "Guru BK", "Expo Kampus", "Alumni", "Mahasiswa", "Situs web resmi IPB", "Platform pencarian kampus online", "Event IPB", "Lainnya"], "required": True},  
    {"id": "pengaruh_memilih", "section": "MASUK KE PRODI MATEMATIKA", "text": "Siapa yang paling berpengaruh dalam keputusanmu memilih Matematika?", "type": "radio", "options": ["Orang tua", "Keluarga", "Guru", "Teman", "Diri sendiri", "Sosmed", "Lainnya"], "required": True},
    {"id": "keraguan", "section": "MASUK KE PRODI MATEMATIKA", "text": "Apakah ada keraguan/kekhawatiran sebelum memutuskan masuk prodi Matematika?", "type": "radio", "options": ["Ya", "Tidak"], "required": True},

    # SECTION: TIPE MATEMATIKA PART II
    {"id": "tipe_6", "section": "TIPE MATEMATIKA PART II", "text": PERSONALITY_QUESTIONS[5]["question"], "type": "personality_quiz", "personality_q_index": 5, "required": True},
    {"id": "tipe_7", "section": "TIPE MATEMATIKA PART II", "text": PERSONALITY_QUESTIONS[6]["question"], "type": "personality_quiz", "personality_q_index": 6, "required": True},
    {"id": "tipe_8", "section": "TIPE MATEMATIKA PART II", "text": PERSONALITY_QUESTIONS[7]["question"], "type": "personality_quiz", "personality_q_index": 7, "required": True},
    {"id": "tipe_9", "section": "TIPE MATEMATIKA PART II", "text": PERSONALITY_QUESTIONS[8]["question"], "type": "personality_quiz", "personality_q_index": 8, "required": True},
    {"id": "tipe_10", "section": "TIPE MATEMATIKA PART II", "text": PERSONALITY_QUESTIONS[9]["question"], "type": "personality_quiz", "personality_q_index": 9, "required": True},

    # SECTION: DI MATEMATIKA
    {"id": "matkul_fav", "section": "DI MATEMATIKA", "text": "Matkul Favorit mu di prodi Matematika apa?", "type": "selectbox", "options": ["Pilih salah satu...", "ALinDas", "GrafAlgo", "KalDu", "KomDas", "MatDis", "PLM", "PDB", "MetStat", "Geonal", "KalTi", "MetNum", "ProgLin", "PTP", "PDP", "AnKom", "Pemod", "PTL", "Prostok", "StatMat", "AnReal", "SA", "MatKrip", "AKM", "SisDim", "PRO"], "required": True},
    {"id": "matkul_susah", "section": "DI MATEMATIKA", "text": "Apa Menurut mu Matkul Tersusah di prodi Matematika?", "type": "selectbox", "options": ["Pilih salah satu...", "ALinDas", "GrafAlgo", "KalDu", "KomDas", "MatDis", "PLM", "PDB", "MetStat", "Geonal", "KalTi", "MetNum", "ProgLin", "PTP", "PDP", "AnKom", "Pemod", "PTL", "Prostok", "StatMat", "AnReal", "SA", "MatKrip", "AKM", "SisDim", "PRO"], "required": True},
    {"id": "jam_belajar", "section": "DI MATEMATIKA", "text": "Berapa Jam yang kamu gunakan untuk belajar per minggu?", "type": "radio", "options": ["G belajar", "1-2", "3-5", "6-10", "11-15", "16-20", "21-25", "26+"], "required": True},  
    {"id": "waktu_luang", "section": "DI MATEMATIKA", "text": "Apa Kegiatan yang kamu lakukan di Waktu Luang? (Boleh pilih lebih dari 1)", "type": "multiselect", "options": ["Belajar", "Nonton Video/Film", "Tidur", "Nongkrong", "Aktif Kegiatan Kampus", "Main Game", "Sosmed", "Lainnya"], "required": True},
    {"id": "pengeluaran", "section": "DI MATEMATIKA", "text": "Biasanya Pengeluaran per Bulan berapa? (tidak harus jawab)", "type": "radio", "options": ["Nggak mau jawab", "<Rp1 000 000", "Rp1 000 000-Rp2 000 000", "Rp2 000 000-Rp2 500 000", "+Rp2 500 000"], "required": True},
    {"id": "menyesal", "section": "DI MATEMATIKA", "text": "Apakah menyesal masuk prodi Matematika?", "type": "radio", "options": ["Sangat Menyesal", "Menyesal", "Netral", "Puas", "Sangat Puas"], "required": True},
    
    # SECTION: TIPE MATEMATIKA PART III
    {"id": "tipe_11", "section": "TIPE MATEMATIKA PART III", "text": PERSONALITY_QUESTIONS[10]["question"], "type": "personality_quiz", "personality_q_index": 10, "required": True},
    {"id": "tipe_12", "section": "TIPE MATEMATIKA PART III", "text": PERSONALITY_QUESTIONS[11]["question"], "type": "personality_quiz", "personality_q_index": 11, "required": True},
    {"id": "tipe_13", "section": "TIPE MATEMATIKA PART III", "text": PERSONALITY_QUESTIONS[12]["question"], "type": "personality_quiz", "personality_q_index": 12, "required": True},
    {"id": "tipe_14", "section": "TIPE MATEMATIKA PART III", "text": PERSONALITY_QUESTIONS[13]["question"], "type": "personality_quiz", "personality_q_index": 13, "required": True},
    {"id": "tipe_15", "section": "TIPE MATEMATIKA PART III", "text": PERSONALITY_QUESTIONS[14]["question"], "type": "personality_quiz", "personality_q_index": 14, "required": True},
]

# --- 3. RESULT CONTENT CONSTANTS ---

PERSONALITY_DESCRIPTIONS = {
    "visioner": {
        "name": "Si Visioner (Murni / Intuitif)",
        "style_html": "<div style='background: linear-gradient(135deg, #818cf8, #6366f1); padding: 36px; border-radius: 20px; color: white; box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);'>",
        "title_html": "<h2 style='color: white; text-align: center; margin-top: 0; margin-bottom: 20px;'>✨ Si Visioner (Murni / Intuitif)</h2>",
        "desc_html": "<p style='font-size: 1.15em; line-height: 1.9;'>"
                     "Lo tertarik sama 'gambaran besar' di matematika abstrak. Lo mungkin mikirnya pake bentuk, struktur, dan hubungan. "
                     "Lo bisa jadi 'ngeliat' jawaban dari masalah jauh sebelum bukti formalnya kelar. "
                     "Lo cocok gaul sama ahli geometri dan topologi yang suka menjelajahi dunia pemikiran baru."
                     "</p>"
    },
    "arsitek": {
        "name": "Si Arsitek (Murni / Formalis)",
        "style_html": "<div style='background: linear-gradient(135deg, #a78bfa, #8b5cf6); padding: 36px; border-radius: 20px; color: white; box-shadow: 0 10px 30px rgba(139, 92, 246, 0.3);'>",
        "title_html": "<h2 style='color: white; text-align: center; margin-top: 0; margin-bottom: 20px;'>🏗️ Si Arsitek (Murni / Formalis)</h2>",
        "desc_html": "<p style='font-size: 1.15em; line-height: 1.9;'>"
                     "Lo itu tipe 'pembangun'. Lo percaya matematika itu kayak bangunan logis yang megah, dibangun dari nol, mulai dari aksioma dan definisi. "
                     "Lo ngerasa keren aja gitu liat bukti yang presisi dan pas. "
                     "Lo cocok gaul sama ahli logika dan aljabar yang mastiin fondasi matematika itu kokoh."
                     "</p>"
    },
    "pemodel": {
        "name": "Si Pemodel (Terapan / Intuitif)",
        "style_html": "<div style='background: linear-gradient(135deg, #f472b6, #ec4899); padding: 36px; border-radius: 20px; color: white; box-shadow: 0 10px 30px rgba(236, 72, 153, 0.3);'>",
        "title_html": "<h2 style='color: white; text-align: center; margin-top: 0; margin-bottom: 20px;'>🎨 Si Pemodel (Terapan / Intuitif)</h2>",
        "desc_html": "<p style='font-size: 1.15em; line-height: 1.9;'>"
                     "Intuisi lo kuat banget buat ngertiin sistem di dunia nyata. Lo bisa liat masalah rumit (di fisika, biologi, atau keuangan) dan "
                     "langsung 'ngeh' pola matematika di baliknya. Lo jago bikin model simpel yang nangkep inti masalahnya, "
                     "biarpun bagian detailnya lo serahin ke orang lain. Lo itu pemecah masalah 'gambaran besar'."
                     "</p>"
    },
    "analis": {
        "name": "Si Analis (Terapan / Formalis)",
        "style_html": "<div style='background: linear-gradient(135deg, #2dd4bf, #14b8a6); padding: 36px; border-radius: 20px; color: white; box-shadow: 0 10px 30px rgba(20, 184, 166, 0.3);'>",
        "title_html": "<h2 style='color: white; text-align: center; margin-top: 0; margin-bottom: 20px;'>⚙️ Si Analis (Terapan / Formalis)</h2>",
        "desc_html": "<p style='font-size: 1.15em; line-height: 1.9;'>"
                     "Lo itu jagonya detail. Lo tau 'kira-kira' aja nggak cukup kalo udah urusan aplikasi di dunia nyata. "
                     "Lo jago di analisis numerik, statistik, dan optimisasi, mastiin model itu nggak cuma jalan, tapi juga akurat, stabil, dan bisa diandelin. "
                     "Lo cocok gaul sama para 'quant' dan insinyur yang bikin dunia modern ini jalan."
                     "</p>"
    }
}

MATHEMATICIAN_DATA = {
    "visioner": [
        {"name": "Bernhard Riemann", "desc": "Ahli geometri yang visioner, menciptakan konsep geometri non-Euclidean yang mengubah pemahaman ruang", "era": "1826-1866"},
        {"name": "Henri Poincaré", "desc": "Polymath yang intuitif, pelopor topologi dan teori chaos dengan intuisi geometri yang luar biasa", "era": "1854-1Dramaga, Bogor"},
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

MATH_FIELD_DATA = {
    "visioner": [
        {"name": "🌀 Topologi", "desc": "Studi tentang bentuk dan ruang yang bertransformasi. Lo bakal suka konsep abstrak seperti manifold, homotopi, dan ruang-ruang eksotis.", "topics": "Topologi Aljabar • Teori Simpul • Manifold"},
        {"name": "🎨 Geometri Diferensial", "desc": "Geometri di permukaan melengkung dengan kalkulus. Perfect buat yang suka visualisasi dan intuisi geometris yang kuat.", "topics": "Kurva & Permukaan • Tensor • Geometri Riemann"},
        {"name": "🔮 Teori Kategori", "desc": "Bahasa abstrak yang menyatukan berbagai cabang matematika. Lo bakal suka pola universal dan struktur di balik struktur.", "topics": "Functor • Natural Transformation • Category Theory"},
        {"name": "🌌 Geometri Aljabar", "desc": "Studi bentuk geometri lewat persamaan aljabar. Kombinasi indah antara visualisasi geometris dan struktur aljabar abstrak.", "topics": "Varieties • Schemes • Cohomology Theory"},
    ],
    "arsitek": [
        {"name": "🏛️ Teori Himpunan & Logika", "desc": "Fondasi dari semua matematika. Lo bakal menikmati membangun matematika dari aksioma dasar dengan presisi sempurna.", "topics": "Aksioma ZFC • Model Theory • Proof Theory"},
        {"name": "🔢 Aljabar Abstrak", "desc": "Studi struktur aljabar murni seperti grup, ring, dan field. Sistematis, elegan, dan beautifully structured.", "topics": "Group Theory • Ring Theory • Galois Theory"},
        {"name": "📐 Teori Bilangan", "desc": "Eksplorasi mendalam sifat bilangan bulat dengan bukti yang rigorous dan elegant. The queen of mathematics.", "topics": "Number Theory • Diophantine Equations • Modular Forms"},
        {"name": "🧩 Kombinatorika", "desc": "Seni menghitung dan menyusun objek diskrit dengan metode yang presisi. Struktur yang elegant dan proof yang beautiful.", "topics": "Graph Theory • Enumerative Combinatorics • Design Theory"},
    ],
    "pemodel": [
        {"name": "🌊 Persamaan Diferensial", "desc": "Model perubahan di dunia nyata - dari cuaca, populasi, hingga aliran fluida. Powerful dan sangat aplikatif.", "topics": "PDE • Dynamical Systems • Chaos Theory"},
        {"name": "🎲 Probabilitas & Stokastik", "desc": "Matematika ketidakpastian untuk finance, machine learning, dan sistem kompleks. Intuitive dan practical.", "topics": "Stochastic Calculus • Random Processes • Markov Chains"},
        {"name": "🤖 Matematika Komputasi", "desc": "Kombinasi matematika dan algoritma untuk AI, data science, dan optimization. Super relevant di era digital.", "topics": "Machine Learning • Graph Theory • Optimization"},
        {"name": "🎯 Riset Operasi", "desc": "Optimasi keputusan di sistem kompleks - supply chain, scheduling, resource allocation. Langsung applicable ke bisnis.", "topics": "Linear Programming • Integer Programming • Network Optimization"},
    ],
    "analis": [
        {"name": "📊 Analisis Numerik", "desc": "Metode presisi tinggi untuk menyelesaikan masalah matematika di komputer. Essential untuk engineering dan science.", "topics": "Numerical Methods • Finite Elements • Error Analysis"},
        {"name": "📈 Analisis Real & Kompleks", "desc": "Studi mendalam tentang fungsi, limit, dan kontinuitas dengan rigorous proofs. Foundation of calculus.", "topics": "Real Analysis • Complex Analysis • Functional Analysis"},
        {"name": "💹 Matematika Keuangan", "desc": "Aplikasi matematika presisi untuk pricing, risk management, dan trading strategies di financial markets.", "topics": "Quantitative Finance • Options Pricing • Risk Models"},
        {"name": "📉 Optimasi & Kontrol", "desc": "Mencari solusi terbaik dengan constraints ketat. Critical untuk engineering, manufacturing, dan logistics.", "topics": "Convex Optimization • Optimal Control • Calculus of Variations"},
    ]
}


# --- 4. HELPER FUNCTIONS ---

def save_to_google_sheets(data_dict):
    """Save quiz results to Google Sheets"""
    try:
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"], scopes=scope
        )
        
        client = gspread.authorize(credentials)
        spreadsheet_url = st.secrets["google_sheets"]["spreadsheet_url"]
        sheet = client.open_by_url(spreadsheet_url).sheet1
        
        existing_headers = sheet.get_all_values()
        new_headers = list(data_dict.keys())
        
        if len(existing_headers) == 0:
            sheet.append_row(new_headers)
        
        # Ensure values are appended in the correct header order
        values = []
        for header in new_headers:
            value = data_dict.get(header, "")
            if isinstance(value, list):
                values.append(", ".join(value))
            else:
                values.append(value)
                
        sheet.append_row(values)
        return True
    except Exception as e:
        st.error(f"Error saving to Google Sheets: {str(e)}")
        return False

def calculate_personality_scores(answers):
    """Calculates the X and Y personality scores based on answers."""
    score_x = 0
    score_y = 0

    for q_config in MASTER_SURVEY_QUESTIONS:
        if q_config["type"] == "personality_quiz":
            q_id = q_config["id"]
            p_q_index = q_config["personality_q_index"]
            p_q = PERSONALITY_QUESTIONS[p_q_index]
            
            answer_text = answers.get(q_id)  
            answer_score = PERSONALITY_OPTIONS.get(answer_text, 0)  
            
            score_x += answer_score * p_q['weights']['x']
            score_y += answer_score * p_q['weights']['y']
            
    return score_x, score_y

def get_personality_details(score_x, score_y):
    """Determines the personality key based on the scores."""
    if score_x < 0:
        return "visioner" if score_y > 0 else "arsitek"
    else:
        return "pemodel" if score_y > 0 else "analis"

def validate_answer(q_config, current_value):
    """Checks if the current answer is valid based on question rules."""
    q_id = q_config["id"]
    q_required = q_config.get("required", False)
    
    if q_required and not current_value:
        return False, "☝️ Harap isi jawaban lo sebelum lanjut."

    # Check if a required selectbox is still on the placeholder
    if q_type == "selectbox" and q_required and current_value == q_config["options"][0]:
        return False, "☝️ Harap isi jawaban lo sebelum lanjut."
        
    if q_id == 'nama' and current_value and not current_value.isupper():
        return False, "Format salah. Nama harus ditulis dengan HURUF KAPITAL."
    
    if q_id == 'nim' and current_value and not current_value.isupper():
        return False, "Format salah. NIM harus ditulis dengan HURUF KAPITAL."
        
    if q_id == 'whatsapp' and current_value and (not current_value.startswith("wa.me/62") or len(current_value) < 13):
        return False, "Format WA salah. Harus: 'wa.me/62...'. Contoh: wa.me/628123456789"
        
    return True, None

def save_answer_callback(q_id):
    """Callback function to save an answer to session state."""
    if q_id in st.session_state:
        st.session_state.answers[q_id] = st.session_state[q_id]

# --- 5. RESULT RENDERING FUNCTIONS ---

def render_score_cards(score_x, score_y):
    """Displays the two cards for X and Y scores."""
    st.markdown("<h2 style='text-align: center;'>Hasil Tipe Matematikawan Lo</h2>", unsafe_allow_html=True)
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"<div class='score-card'>"
            f"<div class='score-label'>Skor X: Murni ↔ Terapan</div>"
            f"<div class='score-value'>{score_x:.1f}</div>"
            f"</div>",
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"<div class='score-card'>"
            f"<div class='score-label'>Skor Y: Formalis ↔ Intuitif</div>"
            f"<div class='score-value'>{score_y:.1f}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

def render_personality_plot(score_x, score_y, plot_limit):
    """Generates and displays the Matplotlib personality plot."""
    fig, ax = plt.subplots(figsize=(11, 11), facecolor='white')
    fig.patch.set_alpha(0.0)
    
    ax.set_xlim(-plot_limit, plot_limit)
    ax.set_ylim(-plot_limit, plot_limit)
    
    ax.grid(True, linestyle='--', alpha=0.2, linewidth=0.8, zorder=0)
    ax.axhline(0, color='#64748b', linewidth=2.5, zorder=1, alpha=0.5)
    ax.axvline(0, color='#64748b', linewidth=2.5, zorder=1, alpha=0.5)
    
    # Quadrant colors
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

def render_personality_description(personality_key):
    """Displays the colored description box for the resulting personality."""
    details = PERSONALITY_DESCRIPTIONS.get(personality_key)
    if details:
        st.markdown(
            f"{details['style_html']}"
            f"{details['title_html']}"
            f"{details['desc_html']}"
            "</div>",
            unsafe_allow_html=True
        )

def render_mathematicians(personality_key):
    """Displays the three related mathematician cards."""
    cols = st.columns(3)
    for idx, math in enumerate(MATHEMATICIAN_DATA.get(personality_key, [])):
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

def render_math_fields(personality_key):
    """Displays the list of related math fields."""
    for field in MATH_FIELD_DATA.get(personality_key, []):
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

def save_and_display_footer(score_x, score_y, personality_name):
    """Saves data to GSheets and shows the final success message and reset button."""
    result_data = {}
    result_data["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Loop through MASTER_SURVEY_QUESTIONS to guarantee order and completeness
    for q_config in MASTER_SURVEY_QUESTIONS:
        q_id = q_config["id"]
        answer = st.session_state.answers.get(q_id)
        
        if isinstance(answer, list):
            result_data[q_id] = ", ".join(answer) # Convert multiselect list
        else:
            result_data[q_id] = answer
            
    # Add the calculated personality scores
    result_data["Skor_X_Murni_Terapan"] = score_x
    result_data["Skor_Y_Formalis_Intuitif"] = score_y
    result_data["Tipe_Matematikawan"] = personality_name
    
    if save_to_google_sheets(result_data):
        st.success("✅ Makasih udah ngisi! Hasil lo udah tersimpan ke database.")
    else:
        st.warning("⚠️ Hasil kuis berhasil ditampilkan, tapi gagal menyimpan ke database.")
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# --- 6. INITIALIZE STATE & PLOT LIMITS ---

if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
    st.session_state.answers = {}

# Calculate max plot limits
max_x = 0
max_y = 0
for q in PERSONALITY_QUESTIONS:
    max_x += abs(q['weights']['x'] * 2)  
    max_y += abs(q['weights']['y'] * 2)
plot_limit = max(max_x, max_y) + 2


# --- 7. MAIN APP EXECUTION ---

load_css()

# --- Banner ---
try:
    st.image("banner.png", use_container_width=True)  
except Exception as e:
    st.warning(f"Tidak dapat memuat banner. Pastikan 'banner.png' ada di root repo. Error: {e}")

# --- Main Content Box ---
st.markdown("<div class='main-container'>", unsafe_allow_html=True)

st.title("📊 Database Karakteristik Matematika")
st.markdown(
    "<div style='text-align: center; color: #f8f9fa; font-size: 1.15em; font-weight: 500;'>"
    "Survey ini bertujuan untuk memetakan karakteristik mahasiswa Matematika IPB. "
    "Data yang kamu berikan akan sangat membantu kami. "
    "Di akhir, kamu akan melihat Tipe Matematikawan kamu! 🎯"
    "</div>",
    unsafe_allow_html=True
)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

total_questions = len(MASTER_SURVEY_QUESTIONS)

# --- Check AppState: QUESTIONS or RESULTS ---

if st.session_state.current_question < total_questions:
    
    # --- 7a. RENDER QUESTIONS ---
    
    # Progress section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        progress = (st.session_state.current_question) / total_questions
        st.progress(min(progress, 0.99))
        st.markdown(
            f"<div style='text-align: center; font-weight: 700; color: #f8f9fa; font-size: 1.1em; margin-top: 12px;'>"
            f"Soal {st.session_state.current_question + 1} dari {total_questions}"
            f"</div>",
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    
    # Get current question config
    q_config = MASTER_SURVEY_QUESTIONS[st.session_state.current_question]
    q_id = q_config["id"]
    q_type = q_config["type"]
    q_text = q_config["text"]
    q_section = q_config["section"]

    # --- Display Section Header ---
    if st.session_state.current_question == 0:
        st.markdown(f"<h2>{q_section}</h2><hr>", unsafe_allow_html=True)
    else:
        prev_section = MASTER_SURVEY_QUESTIONS[st.session_state.current_question - 1]["section"]
        if q_section != prev_section:
            st.markdown(f"<h2>{q_section}</h2><hr>", unsafe_allow_html=True)

    # --- Display Question Subheader ---
    st.subheader(q_text)
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    prev_answer = st.session_state.answers.get(q_id)

    # --- Render the correct widget based on type ---
    
    if q_type == "text_input":
        st.text_input(q_text, value=prev_answer if prev_answer else "", label_visibility="collapsed", key=q_id, on_change=save_answer_callback, args=(q_id,))
            
    elif q_type == "text_area":
        st.text_area(q_text, value=prev_answer if prev_answer else "", label_visibility="collapsed", key=q_id, on_change=save_answer_callback, args=(q_id,))

    elif q_type == "radio":
        options = q_config["options"]
        default_index = None  
        if prev_answer in options:
            default_index = options.index(prev_answer)
            
        st.radio(q_text, options=options, index=default_index, label_visibility="collapsed", key=q_id, on_change=save_answer_callback, args=(q_id,))
    
    elif q_type == "selectbox":
        options = q_config["options"]
        
        # Default to the placeholder (index 0)
        default_index = 0 
        if prev_answer in options:
            # If an answer is already saved, find its index
            default_index = options.index(prev_answer)
            
        st.selectbox(q_text, 
                     options=options, 
                     index=default_index,  # This will now correctly show the saved answer
                     label_visibility="collapsed", 
                     key=q_id, 
                     on_change=save_answer_callback, 
                     args=(q_id,)) 
                     # The placeholder argument is completely removed
        
    elif q_type == "multiselect":
        options = q_config["options"]
        default_value = prev_answer if (prev_answer and isinstance(prev_answer, list)) else []
        st.multiselect(q_text, options=options, default=default_value, label_visibility="collapsed", key=q_id, on_change=save_answer_callback, args=(q_id,), placeholder="Pilih satu atau lebih...")

    elif q_type == "personality_quiz":
        options = list(PERSONALITY_OPTIONS.keys())
        default_index = None  
        if prev_answer in options:
            default_index = options.index(prev_answer)

        st.radio(q_text, options=options, index=default_index, label_visibility="collapsed", key=q_id, on_change=save_answer_callback, args=(q_id,))


    # --- VALIDATION LOGIC ---
    current_value = st.session_state.answers.get(q_id)
    is_valid, validation_message = validate_answer(q_config, current_value)

    if validation_message:
        st.error(validation_message)
        
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    
    # --- Navigation Buttons ---
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("← Sebelumnya", disabled=(st.session_state.current_question == 0), use_container_width=True):
            st.session_state.current_question -= 1
            st.rerun()

    with col3:
        if st.session_state.current_question < total_questions - 1:
            if st.button("Berikutnya →", use_container_width=True, disabled=not is_valid):
                st.session_state.current_question += 1
                st.rerun()
        else:
            if st.button("✨ Lihat Hasil Gue!", use_container_width=True, disabled=not is_valid):
                st.session_state.current_question = total_questions
                st.rerun()

else:
    
    # --- 7b. RENDER RESULTS ---
    
    st.markdown("---")
    
    # Calculate scores and personality
    score_x, score_y = calculate_personality_scores(st.session_state.answers)
    personality_key = get_personality_details(score_x, score_y)
    personality_name = PERSONALITY_DESCRIPTIONS.get(personality_key, {}).get("name", "Tidak Diketahui")

    # Render all result components
    render_score_cards(score_x, score_y)
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    render_personality_plot(score_x, score_y, plot_limit)
    
    st.markdown("---")
    st.markdown("<h3 style='text-align: center; margin-bottom: 30px;'>🎯 Tipe Matematikawan Lo Adalah:</h3>", unsafe_allow_html=True)
    render_personality_description(personality_key)
    
    st.markdown("---")
    st.markdown("<h3 style='text-align: center; margin-bottom: 30px; margin-top: 40px;'>👥 Matematikawan Terkenal yang Cocok dengan Lo</h3>", unsafe_allow_html=True)
    render_mathematicians(personality_key)
    
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; margin-bottom: 30px;'>📚 Cabang Matematika yang Menarik Buat Lo</h3>", unsafe_allow_html=True)
    render_math_fields(personality_key)
    
    st.markdown("---")
    save_and_display_footer(score_x, score_y, personality_name)


# --- 8. FOOTER (outside main container) ---

st.markdown("</div>", unsafe_allow_html=True) # Close .main-container

footer_text = f"Copyright by Departemen Riset dan Analisis GUMATIKA SSMI IPB 2025 | {APP_VERSION}"
st.markdown(
    f"""
    <div style='text-align: center; color: #f8f9fa; font-size: 0.85em; margin-top: 40px; margin-bottom: 10px;'>
        {footer_text}
    </div>
    <div style='text-align: center; color: #adb5bd; font-size: 0.75em; margin-bottom: 20px;'>
        Tidak melihat update terbaru? Coba hard refresh (Ctrl+Shift+R atau Cmd+Shift+R).
    </div>
    """,
    unsafe_allow_html=True
)

import streamlit as st
import joblib
import json
import pandas as pd
import sqlite3
from datetime import datetime

# Setup Database SQLite (Untuk keperluan Skripsi)
def init_db():
    conn = sqlite3.connect('database_gadai.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS riwayat_prediksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            waktu_prediksi TEXT,
            jenis_barang TEXT,
            tipe_barang TEXT,
            tenor INTEGER,
            estimasi_nilai INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Jalankan inisialisasi DB setiap aplikasi dibuka
init_db()

# Konfigurasi halaman
st.set_page_config(
    page_title="Prediksi Nilai Gadai Elektronik",
    page_icon="💰",
    layout="centered"
)

# css custom
st.markdown("""
    <style>
    .stApp {
        background: #f4f7fb;
    }

    .app-title {
        text-align: center;
        color: #1f4f96;
        font-weight: 800;
        font-size: 1.8rem;
        margin-bottom: 0.2rem;
    }
    .app-subtitle {
        text-align: center;
        color: #5f6c80;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }

    label {
        font-weight: 600 !important;
        color: #1f3b5b !important;
    }

    .stButton > button {
        background: linear-gradient(90deg, #2867c9, #1f4f96);
        color: white;
        border-radius: 999px;
        padding: 0.6rem 1.6rem;
        border: none;
        font-weight: 600;
        letter-spacing: 0.02em;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #1f4f96, #143567);
    }

    .result-box {
        margin-top: 1.5rem;
        padding: 1.0rem 1.2rem;
        border-radius: 12px;
        background: #e8f1ff;
        border: 1px solid #c3d6ff;
        color: #0f2b5b;
        font-weight: 600;
        text-align: center;
        font-size: 1.05rem;
    }
    </style>
""", unsafe_allow_html=True)

# Load model & options (var jenis & type)
@st.cache_resource
def load_model():
    model = joblib.load("model/rf_gadai_model.pkl")
    return model

model = load_model()

@st.cache_data
def get_jenis_options():
    conn = sqlite3.connect('database_gadai.db')
    df = pd.read_sql_query("SELECT DISTINCT jenis_barang FROM master_barang ORDER BY jenis_barang", conn)
    conn.close()
    return df['jenis_barang'].tolist()

@st.cache_data
def get_tipe_options(jenis):
    conn = sqlite3.connect('database_gadai.db')
    c = conn.cursor()
    c.execute("SELECT tipe_barang FROM master_barang WHERE jenis_barang = ? ORDER BY tipe_barang", (jenis,))
    rows = c.fetchall()
    conn.close()
    return [r[0] for r in rows]

jenis_options = get_jenis_options()

# UI Utama
st.markdown('<div class="main-card">', unsafe_allow_html=True)

st.markdown('<div class="app-title">Prediksi Nilai Gadai Elektronik</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">Masukkan data barang untuk memperkirakan nilai gadai</div>', unsafe_allow_html=True)

# Input user
col1, col2 = st.columns(2)

with col1:
    selected_jenis = st.selectbox("Jenis Barang", jenis_options)

with col2:
    # Filter type berdasarkan jenis yang dipilih dari database
    type_options = get_tipe_options(selected_jenis)
    if len(type_options) == 0:
        type_options = ["(Belum ada data type untuk jenis ini)"]
    selected_type = st.selectbox("Tipe Barang", type_options)

tenor = st.number_input(
    "Tenor Gadai (hari)",
    min_value=1,
    max_value=180,
    value=30,
    step=1
)

st.write("")

# Tombol prediksi
predict_btn = st.button("Prediksi Nilai Gadai")

if predict_btn:
    input_df = pd.DataFrame(
        {
            "jenis": [selected_jenis],
            "type": [selected_type],
            "tenor": [tenor],
        }
    )

    try:
        pred = model.predict(input_df)[0]
        pred_int = int(pred)

        # Simpan riwayat ke database SQLite
        try:
            conn = sqlite3.connect('database_gadai.db')
            c = conn.cursor()
            
            # Cari id_barang
            c.execute("SELECT id_barang FROM master_barang WHERE jenis_barang=? AND tipe_barang=?", (selected_jenis, selected_type))
            res = c.fetchone()
            id_barang = res[0] if res else None

            waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute("INSERT INTO riwayat_prediksi (waktu_prediksi, id_barang, tenor, estimasi_nilai) VALUES (?, ?, ?, ?)",
                      (waktu_sekarang, id_barang, tenor, pred_int))
            conn.commit()
            conn.close()
        except Exception as e_db:
            print("Gagal menyimpan ke DB:", e_db)

        st.markdown(
            f'<div class="result-box">Estimasi Nilai Gadai: <br><span style="font-size:1.3rem;">Rp {pred_int:,.0f}</span></div>',
            unsafe_allow_html=True
        )
    except Exception as e:
        st.error(f"Terjadi kesalahan saat melakukan prediksi: {e}")

st.markdown('</div>', unsafe_allow_html=True)

st.write("---")
with st.expander("Lihat Riwayat Prediksi (Fitur Admin / Skripsi)"):
    try:
        conn = sqlite3.connect('database_gadai.db')
        query = """
        SELECT r.id, r.waktu_prediksi, m.jenis_barang, m.tipe_barang, r.tenor, r.estimasi_nilai 
        FROM riwayat_prediksi r 
        LEFT JOIN master_barang m ON r.id_barang = m.id_barang 
        ORDER BY r.id DESC
        """
        df_riwayat = pd.read_sql_query(query, conn)
        conn.close()
        
        if len(df_riwayat) > 0:
            st.dataframe(df_riwayat, use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada data riwayat prediksi.")
    except Exception as e:
        st.error(f"Gagal memuat database: {e}")
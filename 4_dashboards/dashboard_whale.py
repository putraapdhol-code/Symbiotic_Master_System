import streamlit as st
import pandas as pd
import os
import time

# --- FUNGSI SMART LOAD (Anti-Gagal di Cloud & Lokal) ---
def load_data_aman(nama_file):
    # Daftar kemungkinan lokasi file
    kemungkinan_lokasi = [
        nama_file,                                      # Lokasi 1: Folder Utama (Root)
        os.path.join("..", nama_file),                 # Lokasi 2: Naik satu tingkat
        os.path.join(os.path.dirname(__file__), "..", nama_file) # Lokasi 3: Alamat Absolut
    ]
    
    for lokasi in kemungkinan_lokasi:
        if os.path.exists(lokasi):
            return pd.read_csv(lokasi)
    return None

# --- MULAI TAMPILAN DASHBOARD ---
st.set_page_config(page_title="Symbiotic Master Intel", layout="wide")
st.title("🐋 Symbiotic Master Intelligence")

# Ambil Data
df_whale = load_data_aman("laporan_whale_continuous.csv")
df_ai = load_data_aman("hasil_prediksi_ai.csv")

# Tampilkan Radar Paus
st.header("🔍 Real-Time Whale Tracker")
if df_whale is not None:
    st.dataframe(df_whale.tail(10), use_container_width=True)
else:
    st.info("Sedang mencari file 'laporan_whale_continuous.csv' di server...")

st.markdown("---")

# Tampilkan AI Analysis
st.header("🧠 AI Market Analysis")
if df_ai is not None:
    st.table(df_ai.drop_duplicates(subset=['Koin'], keep='last'))
else:
    st.warning("Sedang mencari file 'hasil_prediksi_ai.csv' di server...")

# Auto Refresh
time.sleep(10)
st.rerun()
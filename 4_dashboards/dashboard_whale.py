import streamlit as st
import pandas as pd
import os
import time

st.set_page_config(page_title="Symbiotic Master Intel", layout="wide")

st.title("🐋 Symbiotic Master Intelligence")
st.markdown("---")

# --- BAGIAN 1: RADAR PAUS (INFRASTRUCTURE) ---
st.header("🔍 Real-Time Whale Tracker")
path_whale = os.path.join("..", "laporan_whale_continuous.csv")

if os.path.exists(path_whale):
    df_whale = pd.read_csv(path_whale)
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.metric("Total Transaksi Paus", len(df_whale))
        st.metric("Total ETH Berpindah", f"{df_whale['Jumlah_ETH'].sum():,.2f}")
    
    with col2:
        st.write("### Transaksi Terakhir")
        st.dataframe(df_whale.tail(5), use_container_width=True)
else:
    st.info("Menunggu data dari Radar Paus (Folder 3)...")

st.markdown("---")

# --- BAGIAN 2: AI PREDICTION (AI MODELS) ---
st.header("🧠 AI Market Analysis (Multi-Asset)")
path_ai = os.path.join("..", "hasil_prediksi_ai.csv")

if os.path.exists(path_ai):
    df_ai = pd.read_csv(path_ai)
    # Ambil data terbaru untuk setiap koin agar tidak double
    df_latest = df_ai.drop_duplicates(subset=['Koin'], keep='last')
    
    st.table(df_latest) # Pakai table biar terlihat rapi dan formal
else:
    st.warning("Jalankan AI Scanner (Folder 2) untuk memunculkan data di sini.")

# Auto Refresh tiap 10 detik
time.sleep(10)
st.rerun()
# --- BAGIAN PALING BAWAH DASHBOARD ---

# Tambahkan Sidebar untuk Kontrol
st.sidebar.header("Konfigurasi Sistem")
refresh_rate = st.sidebar.slider("Kecepatan Update (Detik)", 5, 60, 10)

st.sidebar.write(f"Terakhir Diperbarui: {time.strftime('%H:%M:%S')}")

# Tombol Manual Refresh
if st.sidebar.button('Refresh Data Sekarang'):
    st.rerun()

# Auto Refresh Logika
time.sleep(refresh_rate)
st.rerun()
import streamlit as st
import pandas as pd
import os
import time

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Symbiotic Master Intel", layout="wide")

# -------------------------------------------------------
# 📂 LOGIKA SMART PATH (TARUH DI SINI)
# -------------------------------------------------------
if os.path.exists("laporan_whale_continuous.csv"):
    path_whale = "laporan_whale_continuous.csv"
else:
    path_whale = os.path.join("..", "laporan_whale_continuous.csv")

if os.path.exists("hasil_prediksi_ai.csv"):
    path_ai = "hasil_prediksi_ai.csv"
else:
    path_ai = os.path.join("..", "hasil_prediksi_ai.csv")
# -------------------------------------------------------

st.title("🐋 Symbiotic Master Intelligence")
st.markdown("---")

# --- BAGIAN 1: RADAR PAUS ---
st.header("🔍 Real-Time Whale Tracker")

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
    st.info(f"Menunggu data dari Radar Paus... (Mencari di: {path_whale})")

st.markdown("---")

# --- BAGIAN 2: AI PREDICTION ---
st.header("🧠 AI Market Analysis (Multi-Asset)")

if os.path.exists(path_ai):
    df_ai = pd.read_csv(path_ai)
    df_latest = df_ai.drop_duplicates(subset=['Koin'], keep='last')
    st.table(df_latest)
else:
    st.warning(f"Jalankan AI Scanner untuk memunculkan data. (Mencari di: {path_ai})")

# Tombol Refresh & Auto Refresh
st.sidebar.header("Konfigurasi")
if st.sidebar.button('Refresh Data'):
    st.rerun()

time.sleep(10)
st.rerun()
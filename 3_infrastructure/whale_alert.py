import requests
import pandas as pd
import time
import os

# Fungsi untuk simulasi/ambil data perpindahan paus (Whale)
def pantau_paus():
    print("🐋 Radar Paus Symbiotic AKTIF... Mencari pergerakan uang raksasa...")
    
    # Path ke folder utama (naik satu level dari folder 3)
    path_csv = os.path.join("..", "laporan_whale_continuous.csv")
    
    # Simulasi data paus (Bisa diganti dengan API Etherscan/WhaleAlert nanti)
    data_paus = {
        "Waktu": [time.strftime("%H:%M:%S")],
        "Pengirim": ["0x742d...44e"],
        "Penerima": ["Binance_Hot_Wallet"],
        "Jumlah_ETH": [1500.50],
        "Nilai_USD": [2945000.00],
        "Status": ["🚨 WHALE ALERT"]
    }
    
    df_baru = pd.DataFrame(data_paus)
    
    # Simpan ke CSV di folder utama (Append mode)
    if not os.path.isfile(path_csv):
        df_baru.to_csv(path_csv, index=False)
    else:
        df_baru.to_csv(path_csv, mode='a', header=False, index=False)
    
    print(f"✅ Data paus berhasil dicatat ke: {path_csv}")

if __name__ == "__main__":
    while True:
        pantau_paus()
        print("😴 Menunggu 10 detik untuk pemindaian berikutnya...")
        time.sleep(10)
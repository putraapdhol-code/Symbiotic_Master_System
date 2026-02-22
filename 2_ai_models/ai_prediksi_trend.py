import os    # <--- Tambahkan ini
import time  # <--- Tambahkan ini
import requests
import pandas as pd
import numpy as np
import urllib3
from sklearn.ensemble import RandomForestClassifier

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def latih_ai_trading(simbol):
    print("\n" + "="*50)
    print(f"🧠 Memulai Riset AI & Matematika untuk {simbol}...")
    
    # 1. SMART ROUTING
    if simbol == "HYPE-USDT":
        url = "https://api.gateio.ws/api/v4/spot/candlesticks?currency_pair=HYPE_USDT&interval=1h"
        bursa = "Gate.io"
    else:
        url = f"https://api.kucoin.com/api/v1/market/candles?type=1hour&symbol={simbol}"
        bursa = "KuCoin"

    df = None 
    
    # 2. RETRY MECHANISM
    for percobaan in range(3):
        try:
            topeng = {'User-Agent': 'Mozilla/5.0'}
            respons = requests.get(url, headers=topeng, verify=False, timeout=10)
            data = respons.json()
            
            if bursa == "KuCoin" and data.get('code') == '200000' and data.get('data'):
                df = pd.DataFrame(data['data'], columns=['waktu', 'open', 'close', 'high', 'low', 'volume', 'turnover'])
                break 
            elif bursa == "Gate.io" and isinstance(data, list):
                df = pd.DataFrame(data, columns=['waktu', 'volume', 'close', 'high', 'low', 'open', 'amount', 'temp'])
                break 
            else:
                print(f"⚠️ Data {simbol} formatnya tidak sesuai.")
                return
        except Exception as e:
            print(f"⏳ Mencoba ulang {simbol}... ({e})")
            time.sleep(2)

    if df is None or df.empty:
        print(f"❌ Gagal mendapatkan data {simbol}.")
        return

    # 3. PERHITUNGAN MATEMATIKA & AI
    try:
        df['close'] = df['close'].astype(float)
        df['volume'] = df['volume'].astype(float)
        if bursa == "KuCoin":
            df = df.iloc[::-1].reset_index(drop=True)

        df['SMA_20'] = df['close'].rolling(window=20).mean()
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI_14'] = 100 - (100 / (1 + rs))
        
        df['Target'] = (df['close'].shift(-1) > df['close']).astype(int)
        df = df.dropna()
        
        X = df[['close', 'volume', 'SMA_20', 'RSI_14']]
        y = df['Target']
        
        model_ai = RandomForestClassifier(n_estimators=100, random_state=42)
        model_ai.fit(X, y)
        
        data_jam_ini = X.iloc[-1:]
        prediksi = model_ai.predict(data_jam_ini)[0]
        
        harga_sekarang = df['close'].iloc[-1]
        rsi_sekarang = df['RSI_14'].iloc[-1]
        sma_sekarang = df['SMA_20'].iloc[-1]
        
        print(f"✅ Sukses menarik data asli dari {bursa}!")
        print(f"Harga Saat Ini      : ${harga_sekarang:,.4f}")
        print(f"Batas Rata-Rata SMA : ${sma_sekarang:,.4f}")
        print(f"Tingkat RSI         : {rsi_sekarang:.2f}")
        
        label_prediksi = "BULLISH 📈" if prediksi == 1 else "BEARISH 📉"
        print(f"📢 KEPUTUSAN AI: {label_prediksi}")

        # ---------------------------------------------------------
        # 📂 BAGIAN PENYIMPANAN KE CSV (YANG BIKIN BINGUNG TADI)
        # ---------------------------------------------------------
        path_ai = os.path.join("..", "hasil_prediksi_ai.csv")
        data_ai = {
            "Waktu": [time.strftime("%H:%M:%S")],
            "Koin": [simbol],
            "Harga": [f"${harga_sekarang:,.2f}"],
            "RSI": [round(rsi_sekarang, 2)],
            "Prediksi": [label_prediksi]
        }
        df_ai = pd.DataFrame(data_ai)
        
        if not os.path.isfile(path_ai):
            df_ai.to_csv(path_ai, index=False)
        else:
            df_ai.to_csv(path_ai, mode='a', header=False, index=False)
        
        print(f"💾 Hasil prediksi disimpan ke: {path_ai}")

    except Exception as e:
        print(f"❌ Terjadi kesalahan pada {simbol}: {e}")

# ==========================================
# 🚀 PUSAT KOMANDO (Koin HYPE Dimasukkan!)
# ==========================================
daftar_koin = ["BTC-USDT", "ETH-USDT", "SOL-USDT", "BNB-USDT", "HYPE-USDT"]

print("🚀 MEMULAI PEMINDAIAN PASAR MASSAL OLEH AI...")
time.sleep(1)

for koin in daftar_koin:
    latih_ai_trading(koin)
    time.sleep(2) # Jeda agar bursa tidak marah

print("\n✅ PEMINDAIAN PASAR SELESAI!")
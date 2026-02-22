import requests
import pandas as pd
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def intip_orderbook(simbol="ETH-USDT", kedalaman=5):
    print(f"📡 Menghubungkan satelit ke bursa KUCOIN untuk koin {simbol}...")
    
    # 🔑 KuCoin sangat cepat dan jarang diblokir di Indonesia
    url = f"https://api.kucoin.com/api/v1/market/orderbook/level2_20?symbol={simbol}"
    
    try:
        # Tambahkan timeout=5 agar tidak hanging (maksimal nunggu 5 detik)
        headers = {'User-Agent': 'Mozilla/5.0'}
        respons = requests.get(url, headers=headers, verify=False, timeout=5)
        data = respons.json()
        
        if data.get('code') != '200000':
            print("⚠️ Gagal narik data. Balasan server:", data)
            return
            
        # Ambil data antrean
        bids = data['data']['bids'][:kedalaman] # Ambil 5 teratas
        asks = data['data']['asks'][:kedalaman]
        
        df_bids = pd.DataFrame(bids, columns=['Harga_Beli ($)', 'Jumlah_ETH']).astype(float)
        df_asks = pd.DataFrame(asks, columns=['Harga_Jual ($)', 'Jumlah_ETH']).astype(float)
        
        print("\n🟩 TOP 5 ANTREAN BELI (BIDS) - Tembok Penahan Harga Turun:")
        print(df_bids.to_string(index=False))
        
        print("\n🟥 TOP 5 ANTREAN JUAL (ASKS) - Tembok Penahan Harga Naik:")
        print(df_asks.to_string(index=False))
        
        total_beli = df_bids['Jumlah_ETH'].sum()
        total_jual = df_asks['Jumlah_ETH'].sum()
        
        print("\n" + "="*50)
        print("💡 INSIGHT KEDALAMAN PASAR (ORDER BOOK DETIK INI):")
        if total_beli > total_jual:
            print(f"Permintaan lebih kuat! Ada antrean BELI sebesar {total_beli:.2f} ETH.")
        else:
            print(f"Tekanan jual lebih kuat! Ada antrean JUAL sebesar {total_jual:.2f} ETH.")
        print("="*50)

    except requests.exceptions.Timeout:
        print("❌ Server kelamaan balasnya (Timeout)! Coba koneksi internet lain.")
    except Exception as e:
        print(f"❌ Terjadi kesalahan sistem: {e}")

# Eksekusi kodenya!
intip_orderbook("ETH-USDT", 5)
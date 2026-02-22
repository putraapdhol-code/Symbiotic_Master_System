# 🚀 Symbiotic Master Intelligence System
Sistem pemantauan pasar kripto terintegrasi menggunakan AI dan Data Pipeline Real-time.

## 🛠️ Fitur Utama
- **AI Scanner**: Prediksi tren harga menggunakan Random Forest (BTC, ETH, SOL, BNB, HYPE).
- **Whale Tracker**: Monitoring transaksi besar secara terus menerus.
- **Central Dashboard**: Visualisasi data berbasis Web (Streamlit).

## 🏃‍♂️ Cara Menjalankan
1. `pip install -r requirements.txt`
2. Jalankan Radar: `python 3_infrastructure/whale_alert.py`
3. Jalankan AI: `python 2_ai_models/ai_prediksi_trend.py`
4. Buka Web: `streamlit run 4_dashboards/dashboard_whale.py`
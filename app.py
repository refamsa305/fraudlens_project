import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.ensemble import IsolationForest

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="FraudLens - Sistem Deteksi Anomali",
    page_icon="🕵️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS STYLING (Tampilan Modern) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .gradient-text {
        background: linear-gradient(45deg, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. NAVIGASI OTOMATIS (SESSION STATE) ---
if 'page' not in st.session_state:
    st.session_state.page = "🏠 Beranda"

def navigate_to_analysis():
    st.session_state.page = "📊 Analisis Data"

# --- 4. FUNGSI LOGIKA (BACKEND) ---
def calculate_benford(series):
    first_digits = series.astype(str).str.lstrip().str[0]
    first_digits = first_digits[first_digits.str.isnumeric()].astype(int)
    first_digits = first_digits[first_digits > 0]
    obs_counts = first_digits.value_counts(normalize=True).sort_index()
    benford_probs = [np.log10(1 + 1/d) for d in range(1, 10)]
    return pd.DataFrame({
        'Digit': range(1, 10),
        'Benford': benford_probs,
        'Aktual': [obs_counts.get(d, 0) for d in range(1, 10)]
    })

# --- 5. SIDEBAR MENU ---
with st.sidebar:
    try:
        # Ganti URL ini dengan st.image("logo_anda.png") jika punya file lokal
        st.image("logo_anda.png", width=200)
    except:
        st.write("Logo")
    
    st.markdown("## **FraudLens**")
    st.caption("Sistem Audit Cerdas UMKM v2.0")
    st.write("---")
    
    # Menu Navigasi (Terkoneksi dengan tombol Home)
    selected = st.radio(
        "Menu Utama",
        ["🏠 Beranda", "📖 Panduan Pengguna", "📊 Analisis Data", "📚 Metode & Teori"],
        key="page" 
    )
    
    st.write("---")
    st.info("💡 **Tips:** Pastikan file Excel Anda memiliki kolom 'Nominal' atau 'Jumlah' uang.")

# --- 6. KONTEN HALAMAN ---

# === HALAMAN 1: BERANDA ===
if selected == "🏠 Beranda":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<h1 class='gradient-text'>Selamat Datang di FraudLens!</h1>", unsafe_allow_html=True)
        st.write("### Partner Cerdas untuk Keuangan yang Transparan.")
        st.write("""
        FraudLens adalah platform audit digital yang dirancang untuk membantu Anda mendeteksi ketidakwajaran 
        dalam laporan keuangan secara cepat, akurat, dan otomatis menggunakan metode Hybrid (Statistik & AI).
        """)
        
        st.write("")
        # Tombol ini sekarang otomatis pindah ke halaman Analisis
        if st.button("Mulai Analisis Sekarang", on_click=navigate_to_analysis):
            pass 
            
    with col2:
        st.image("ilustrasi.png", caption="Digital Audit Illustration")

    st.divider()
    
    st.markdown("### Mengapa Menggunakan FraudLens?")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="glass-card">
            <h4>⚡ Cepat & Otomatis</h4>
            <p>Tidak perlu mengecek ribuan baris Excel satu per satu. Biarkan algoritma yang bekerja dalam hitungan detik.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="glass-card">
            <h4>🛡️ Metode Hybrid</h4>
            <p>Menggabungkan ketepatan Statistik (Benford's Law) dan kecerdasan Machine Learning (Isolation Forest).</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="glass-card">
            <h4>📊 Visualisasi Jelas</h4>
            <p>Hasil analisis disajikan dalam bentuk grafik interaktif yang mudah dipahami oleh orang awam.</p>
        </div>
        """, unsafe_allow_html=True)

# === HALAMAN 2: PANDUAN PENGGUNA (FULL VERSION) ===
elif selected == "📖 Panduan Pengguna":
    st.header("📖 Tutorial Penggunaan Platform")
    st.markdown("Ikuti langkah-langkah berikut untuk melakukan audit mandiri:")
    
    with st.expander("Langkah 1: Persiapan Data", expanded=True):
        st.write("""
        1.  Siapkan laporan keuangan Anda dalam format **Excel (.xlsx)** atau **CSV**.
        2.  Pastikan data memiliki **Header** (baris pertama adalah nama kolom).
        3.  **Wajib:** Harus ada satu kolom yang berisi angka uang (Misal nama kolomnya: *Nominal, Debit, Kredit, atau Amount*).
        """)
        
    with st.expander("Langkah 2: Upload Data"):
        st.write("""
        1.  Masuk ke menu **📊 Analisis Data** (bisa klik tombol di Beranda atau lewat Sidebar).
        2.  Klik tombol **Browse files** atau seret file Anda ke kotak upload yang disediakan.
        3.  Tunggu sesaat hingga muncul notifikasi hijau "File berhasil dimuat!".
        """)

    with st.expander("Langkah 3: Konfigurasi & Scan"):
        st.write("""
        1.  Perhatikan kotak **'Pilih Kolom Nominal'**. Pilih nama kolom yang berisi uang dari data Anda.
        2.  Setelah dipilih, grafik **Hukum Benford** akan otomatis muncul.
        3.  Untuk analisis mendalam, gulir ke bawah dan klik tombol merah **🚀 Scan Anomali Sekarang**.
        """)

    with st.expander("Langkah 4: Membaca Hasil"):
        st.write("""
        * **Grafik Benford:** Perhatikan skor MAD.
            * **Hijau (< 0.05):** Data Wajar/Aman.
            * **Merah (> 0.05):** Indikasi Manipulasi Tinggi.
        * **Tabel Anomali (AI):**
            * Sistem akan menampilkan daftar transaksi dengan skor **-1**.
            * Ini adalah transaksi yang 'terisolasi' atau berbeda jauh dari pola umum. Silakan cek manual transaksi tersebut (apakah salah input atau memang fraud).
        """)

# === HALAMAN 3: ANALISIS DATA (DENGAN SCROLL FIX) ===
elif selected == "📊 Analisis Data":
    st.title("📊 Dashboard Analisis")
    
    uploaded_file = st.file_uploader("Upload Laporan Keuangan (Excel/CSV)", type=["xlsx", "csv"])
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success("File berhasil dimuat!")
            
            # --- INFO RINGKASAN DATA ---
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Baris Data", f"{len(df)} Baris")
            m2.metric("Total Kolom", f"{len(df.columns)} Kolom")
            
            # Pilih Kolom
            numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
            target_col = st.selectbox("🎯 Pilih Kolom Nominal (Uang) untuk dianalisis:", numeric_cols)
            
            if target_col:
                total_uang = df[target_col].sum()
                m3.metric("Total Nominal", f"Rp {total_uang:,.0f}")
            
            # --- TABEL DATA MENTAH (BISA DI-SCROLL) ---
            st.write("### 📋 Preview Data Mentah")
            with st.expander("Klik untuk melihat/menyembunyikan tabel data", expanded=True):
                # height=400 membuat area scroll fixed
                st.dataframe(df, height=400, use_container_width=True)

            if target_col:
                clean_data = df[df[target_col] > 0].copy()
                st.divider()
                
                # --- TAB UNTUK HASIL ANALISIS ---
                tab1, tab2 = st.tabs(["🔍 Analisis Benford (Statistik)", "🤖 AI Anomaly Detector"])
                
                with tab1:
                    st.subheader("Uji Kepatuhan Hukum Benford")
                    st.write("Analisis ini membandingkan frekuensi digit pertama data Anda dengan standar alami.")
                    
                    df_benford = calculate_benford(clean_data[target_col])
                    mad = (df_benford['Aktual'] - df_benford['Benford']).abs().mean()
                    
                    c_chart, c_res = st.columns([3, 1])
                    with c_chart:
                        fig = go.Figure()
                        fig.add_trace(go.Bar(x=df_benford['Digit'], y=df_benford['Aktual'], name='Data Aktual', marker_color='#3b82f6'))
                        fig.add_trace(go.Scatter(x=df_benford['Digit'], y=df_benford['Benford'], name='Benford Ideal', line=dict(color='red', width=3)))
                        st.plotly_chart(fig, use_container_width=True)
                    with c_res:
                        st.metric("Skor MAD", f"{mad:.4f}")
                        if mad > 0.05:
                            st.error("⚠️ HIGH RISK\nIndikasi Manipulasi")
                        else:
                            st.success("✅ LOW RISK\nWajar / Alami")

                with tab2:
                    st.subheader("Deteksi Transaksi Mencurigakan (AI)")
                    st.write("Menggunakan algoritma *Isolation Forest* untuk mencari transaksi yang menyimpang (outlier).")
                    
                    if st.button("🚀 Scan Anomali Sekarang", type="primary"):
                        with st.spinner("Sedang memindai..."):
                            model = IsolationForest(contamination=0.05, random_state=42)
                            clean_data['score'] = model.fit_predict(clean_data[[target_col]])
                            anomalies = clean_data[clean_data['score'] == -1]
                            
                            st.warning(f"Ditemukan {len(anomalies)} transaksi outlier dari total {len(clean_data)} data.")
                            
                            st.write("daftar transaksi yang dicurigai:")
                            st.dataframe(anomalies.style.background_gradient(subset=[target_col], cmap='Reds'), use_container_width=True)
                            
                            st.write("Visualisasi Sebaran Data:")
                            fig_sc = px.scatter(clean_data, x=clean_data.index, y=target_col, color=clean_data['score'].astype(str), 
                                              color_discrete_map={'-1':'red', '1':'grey'}, title="Merah = Anomali / Dicurigai")
                            st.plotly_chart(fig_sc, use_container_width=True)

        except Exception as e:
            st.error(f"Error: {e}")

# === HALAMAN 4: METODE & TEORI (FULL VERSION) ===
elif selected == "📚 Metode & Teori":
    st.header("📚 Landasan Ilmiah")
    
    # --- TAB 1: BENFORD ---
    st.subheader("A. Hukum Benford (Benford's Law)")
    st.write("""
    Hukum Benford menyatakan bahwa dalam kumpulan data numerik alami (seperti transaksi keuangan), 
    digit pertama angka-angka tersebut tidak muncul secara acak, melainkan mengikuti pola tertentu.
    Digit kecil (1, 2) jauh lebih sering muncul daripada digit besar (8, 9).
    """)
    
    st.markdown("**Rumus Probabilitas:**")
    st.latex(r''' P(d) = \log_{10} \left( 1 + \frac{1}{d} \right) ''')
    
    st.markdown("**Tabel Distribusi Probabilitas Benford:**")
    # Tabel manual agar rapi
    benford_data = {
        'Digit Awal': [1, 2, 3, 4, 5, 6, 7, 8, 9],
        'Probabilitas (%)': ['30.1%', '17.6%', '12.5%', '9.7%', '7.9%', '6.7%', '5.8%', '5.1%', '4.6%']
    }
    st.table(pd.DataFrame(benford_data))
    
    st.divider()
    
    # --- TAB 2: ISOLATION FOREST ---
    st.subheader("B. Algoritma Isolation Forest")
    st.write("""
    Isolation Forest adalah algoritma *Unsupervised Machine Learning* yang dirancang khusus untuk mendeteksi anomali. 
    Algoritma ini sangat efisien untuk data berdimensi tinggi.
    """)
    
    st.markdown("#### 🔄 Cara Kerja Algoritma (Runtut):")
    st.markdown("""
    1.  **Sub-sampling:** Algoritma mengambil sebagian sampel data secara acak dari dataset.
    2.  **Partisi Acak (Random Partitioning):**
        * Algoritma memilih satu fitur (kolom) secara acak.
        * Algoritma memilih nilai pemisah (*split value*) secara acak di antara nilai minimum dan maksimum.
        * Data dipotong terus menerus seperti memotong kue.
    3.  **Perhitungan Jalur (Path Length):**
        * Algoritma menghitung berapa kali potongan yang dibutuhkan untuk mengisolasi sebuah titik data (membuatnya sendirian).
        * **Data Normal:** Butuh banyak potongan (jalur panjang) karena mereka bergerombol.
        * **Data Anomali:** Butuh sedikit potongan (jalur pendek) karena nilainya jauh berbeda dan terpencil.
    4.  **Penentuan Skor (Scoring):**
        * Semakin pendek jalurnya (cepat terisolasi), semakin tinggi skor anomalinya (mendekati -1).
        * Sistem FraudLens menandai skor -1 sebagai **Suspect Fraud**.
    """)
    
    st.info("""
    **Analogi Sederhana:**
    Bayangkan Anda mengupas kentang. Kentang yang bentuknya aneh (benjol) akan terkena pisau lebih dulu (mudah dipisahkan). 
    Kentang yang bulat sempurna akan terkupas belakangan karena sulit dibedakan. 
    **Data anomali adalah "kentang benjol" tersebut.**
    """)
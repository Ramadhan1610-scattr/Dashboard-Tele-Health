import streamlit as st
import pandas as pd

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Telemedicine Dashboard", layout="wide", page_icon="🏥")

# --- DATABASE SEDERHANA (SESSION STATE) ---
# Menggunakan session state agar data tersimpan selama aplikasi running
if 'data_pasien' not in st.session_state:
    st.session_state['data_pasien'] = []

# --- SIDEBAR NAVIGASI ---
st.sidebar.title("Telemedicine Menu")
menu = st.sidebar.radio("Pilih Halaman:", ["🏠 Beranda", "📝 Pendaftaran Pasien", "👨‍⚕️ Dashboard Dokter", "📋 Riwayat Resep"])

# --- HALAMAN: BERANDA ---
if menu == "🏠 Beranda":
    st.title("🏥 Sistem Telemedicine Klinik")
    st.write("Selamat datang di sistem manajemen kesehatan jarak jauh sederhana.")
    st.info("Gunakan menu di samping kiri untuk memulai pendaftaran atau pemeriksaan.")
    
    # Statistik sederhana
    col1, col2 = st.columns(2)
    col1.metric("Total Pasien", len(st.session_state['data_pasien']))
    col2.metric("Status Server", "Online")

# --- HALAMAN: PENDAFTARAN ---
elif menu == "📝 Pendaftaran Pasien":
    st.header("Form Registrasi Pasien")
    with st.form(key='form_reg', clear_on_submit=True):
        nama = st.text_input("Nama Lengkap")
        usia = st.number_input("Usia", min_value=0, max_value=120)
        keluhan = st.text_area("Keluhan Utama")
        submit = st.form_submit_button("Daftar Sekarang")
        
        if submit:
            if nama and keluhan:
                new_pasien = {
                    "ID": len(st.session_state['data_pasien']) + 1,
                    "Nama": nama,
                    "Usia": usia,
                    "Keluhan": keluhan,
                    "Diagnosa": "Belum diperiksa",
                    "Resep": "Belum ada resep"
                }
                st.session_state['data_pasien'].append(new_pasien)
                st.success(f"Pasien {nama} berhasil terdaftar di sistem!")
            else:
                st.error("Mohon isi nama dan keluhan!")

# --- HALAMAN: DOKTER ---
elif menu == "👨‍⚕️ Dashboard Dokter":
    st.header("Halaman Diagnosa & Konsultasi")
    if not st.session_state['data_pasien']:
        st.warning("Belum ada antrean pasien.")
    else:
        # Menampilkan tabel antrean
        df = pd.DataFrame(st.session_state['data_pasien'])
        st.subheader("Daftar Antrean")
        st.dataframe(df[['ID', 'Nama', 'Keluhan']])
        
        st.divider()
        
        # Form Input Diagnosa
        st.subheader("Input Hasil Pemeriksaan")
        with st.form(key='form_diag'):
            pilih_nama = st.selectbox("Pilih Pasien", [p['Nama'] for p in st.session_state['data_pasien']])
            diagnosa = st.text_input("Hasil Diagnosa")
            resep = st.text_area("Resep Obat")
            save = st.form_submit_button("Simpan Diagnosa")
            
            if save:
                for p in st.session_state['data_pasien']:
                    if p['Nama'] == pilih_nama:
                        p['Diagnosa'] = diagnosa
                        p['Resep'] = resep
                st.success(f"Diagnosa untuk {pilih_nama} telah diperbarui!")

# --- HALAMAN: RIWAYAT ---
elif menu == "📋 Riwayat Resep":
    st.header("Data Rekam Medis & Resep Digital")
    if st.session_state['data_pasien']:
        df_final = pd.DataFrame(st.session_state['data_pasien'])
        st.table(df_final)
    else:
        st.info("Belum ada data rekam medis.")
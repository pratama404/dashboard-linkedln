import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Dashboard Mahasiswa x LinkedIn 🇮🇩", page_icon="📊", layout="wide")

st.title("📊 Dashboard Mahasiswa Indonesia & Pengguna LinkedIn")
st.caption("Unggah file Anda sendiri atau gunakan data contoh yang sudah disertakan.")

with st.sidebar:
    st.header("⚙️ Pengaturan")
    st.write("Unggah dataset (opsional). Template kolom ada di bawah.")
    up_students = st.file_uploader("students.csv (region, level, year, students)", type=["csv"], key="stud")
    up_age = st.file_uploader("linkedin_age.csv (age_group, users_million, period)", type=["csv"], key="age")
    up_monthly = st.file_uploader("linkedin_monthly.csv (date, users_million)", type=["csv"], key="mon")
    st.markdown("---")
    st.markdown("**Template Kolom:**")
    st.code("students.csv: region, level, year, students\nlinkedin_age.csv: age_group, users_million, period\nlinkedin_monthly.csv: date, users_million")

# Load data (fallback to bundled samples)
def load_csv(path, uploaded_file=None, parse_dates=None):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_csv(path)
    if parse_dates:
        for col in parse_dates:
            df[col] = pd.to_datetime(df[col])
    return df

students = load_csv("students.csv", up_students)
age = load_csv("linkedin_age.csv", up_age)
monthly = load_csv("linkedin_monthly.csv", up_monthly, parse_dates=["date"])

# Basic numbers
total_students = int(students.loc[students["region"]=="Indonesia"].query("level=='Total'")["students"].sum())
users_18_24 = float(age.loc[age["age_group"]=="18-24", "users_million"].values[0])
users_25_34 = float(age.loc[age["age_group"]=="25-34", "users_million"].values[0])
total_linkedin = float(monthly.sort_values("date")["users_million"].iloc[-1])

col1, col2, col3, col4 = st.columns(4)
col1.metric("Mahasiswa (perkiraan)", f"{total_students/1e6:.1f} Juta")
col2.metric("LinkedIn (18–24)", f"{users_18_24:.1f} Juta")
col3.metric("LinkedIn (25–34)", f"{users_25_34:.1f} Juta")
col4.metric("Total Pengguna LinkedIn", f"{total_linkedin:.1f} Juta")

st.markdown("---")

# Row 1: Students by region / level (bar & treemap)
c1, c2 = st.columns((1.2, 0.8))
with c1:
    st.subheader("Distribusi Mahasiswa per Wilayah (Bar)")
    reg = students[students["level"]=="Total"].sort_values("students", ascending=False)
    fig = px.bar(reg, x="region", y="students", labels={"students":"Mahasiswa"}, title=None)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Komposisi Jenjang Pendidikan (Treemap)")
    lv = students[students["region"]=="Indonesia"].query("level!='Total'")
    fig2 = px.treemap(lv, path=["level"], values="students")
    st.plotly_chart(fig2, use_container_width=True)

# Row 2: LinkedIn by age (bar + pie)
c3, c4 = st.columns((1.1, 0.9))
with c3:
    st.subheader("Pengguna LinkedIn per Kelompok Usia")
    fig3 = px.bar(age, x="age_group", y="users_million", labels={"users_million":"Juta Pengguna"})
    st.plotly_chart(fig3, use_container_width=True)
with c4:
    st.subheader("Proporsi Usia (Pie)")
    fig4 = px.pie(age, names="age_group", values="users_million", hole=0.35)
    st.plotly_chart(fig4, use_container_width=True)

# Row 3: Trend & Penetrasi
st.subheader("Tren Pengguna LinkedIn (Bulanan)")
fig5 = px.line(monthly.sort_values("date"), x="date", y="users_million", markers=True,
               labels={"users_million":"Juta Pengguna", "date":"Tanggal"})
st.plotly_chart(fig5, use_container_width=True)

st.subheader("Perbandingan: Mahasiswa vs LinkedIn 18–24")
penetration = (users_18_24*1e6) / total_students if total_students else np.nan
comp_df = pd.DataFrame({
    "Kategori": ["Mahasiswa (18–24, perkiraan total)", "LinkedIn 18–24"],
    "Jumlah": [total_students/1e6, users_18_24]
})
fig6 = px.bar(comp_df, x="Kategori", y="Jumlah", text="Jumlah", labels={"Jumlah":"Juta"})
st.plotly_chart(fig6, use_container_width=True)
st.caption(f"Perkiraan penetrasi LinkedIn pada mahasiswa 18–24: **{penetration*100:.1f}%** (indikatif, sesuaikan dengan data resmi).")

st.markdown("---")
st.markdown("**Catatan:** Angka contoh disediakan agar dashboard tetap berjalan. Silakan ganti dengan data resmi dari Satu Data, data.go.id, GoodStats, NapoleonCat, dll.")

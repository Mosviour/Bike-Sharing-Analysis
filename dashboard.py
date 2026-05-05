import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =====================
# LOAD DATA
# =====================
df_day = pd.read_csv('day_clean.csv')
df_hour = pd.read_csv('hour_clean.csv')

df_day['date'] = pd.to_datetime(df_day['date'])
df_hour['date'] = pd.to_datetime(df_hour['date'])

# =====================
# SIDEBAR
# =====================
min_date = df_day['date'].min()
max_date = df_day['date'].max()

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

    date_input = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

start_date = pd.Timestamp(date_input[0])
end_date = pd.Timestamp(date_input[1]) if len(date_input) > 1 else pd.Timestamp(max_date)

# Filter dataframe
df_filtered = df_day[
    (df_day['date'] >= start_date) &
    (df_day['date'] <= end_date)
]

df_hour_filtered = df_hour[
    (df_hour['date'] >= start_date) &
    (df_hour['date'] <= end_date)
]

# =====================
# JUDUL DASHBOARD
# =====================
st.title('Bike Sharing Dashboard 🚲')
st.markdown('Analisis data peminjaman sepeda periode 2011-2012')

# =====================
# OVERVIEW
# =====================
st.subheader('Overview')
col1, col2, col3 = st.columns(3)
with col1:
    st.metric('Total Peminjaman', f"{df_filtered['total_rentals'].sum():,}")
with col2:
    st.metric('Rata-rata Harian', f"{df_filtered['total_rentals'].mean():.0f}")
with col3:
    st.metric('Hari Tertinggi', f"{df_filtered['total_rentals'].max():,}")

st.markdown('---')

# =====================
# VISUALISASI 1 - Pengaruh Cuaca
# =====================
st.subheader('Pertanyaan 1: Pengaruh Kondisi Cuaca Terhadap Peminjaman Sepeda')

weather_avg = df_filtered.groupby('weather_condition', observed=True)['total_rentals'].mean().reset_index()

fig1, ax1 = plt.subplots(figsize=(10, 6))
colors_weather = ['#66BB6A', '#FFA726', '#EF5350']
sns.barplot(data=weather_avg, x='weather_condition',
            y='total_rentals', palette=colors_weather, ax=ax1)
ax1.set_title('Rata-rata Peminjaman Sepeda Berdasarkan Kondisi Cuaca',
              loc='center', fontsize=15)
ax1.set_xlabel('Kondisi Cuaca', fontsize=12)
ax1.set_ylabel('Rata-rata Total Peminjaman', fontsize=12)
ax1.tick_params(axis='x', labelsize=12)
ax1.tick_params(axis='y', labelsize=12)
for container in ax1.containers:
    ax1.bar_label(container, fmt='%.0f', padding=3, fontsize=12)
plt.tight_layout()
st.pyplot(fig1)

st.markdown('---')

# =====================
# VISUALISASI 2 - Pengaruh Musim
# =====================
st.subheader('Pertanyaan 2: Pengaruh Musim Terhadap Peminjaman Sepeda')

season_avg = df_filtered.groupby('season', observed=True)['total_rentals'].mean().reset_index()

fig2, ax2 = plt.subplots(figsize=(10, 6))
colors_season = ['#D3D3D3', '#90CAF9', '#66BB6A', '#FFA726']
sns.barplot(data=season_avg, x='season',
            y='total_rentals', palette=colors_season, ax=ax2)
ax2.set_title('Rata-rata Peminjaman Sepeda Berdasarkan Musim',
              loc='center', fontsize=15)
ax2.set_xlabel('Musim', fontsize=12)
ax2.set_ylabel('Rata-rata Total Peminjaman', fontsize=12)
ax2.tick_params(axis='x', labelsize=12)
ax2.tick_params(axis='y', labelsize=12)
for container in ax2.containers:
    ax2.bar_label(container, fmt='%.0f', padding=3, fontsize=12)
plt.tight_layout()
st.pyplot(fig2)

st.markdown('---')

# =====================
# VISUALISASI 3 - Hari Kerja vs Libur
# =====================
st.subheader('Pertanyaan 3: Rata-rata Peminjaman Hari Kerja vs Hari Libur')

workingday_avg = df_filtered.groupby('workingday', observed=True)['total_rentals'].mean().reset_index()
workingday_avg['workingday'] = workingday_avg['workingday'].map({
    0: 'Hari Libur',
    1: 'Hari Kerja'
})

fig3, ax3 = plt.subplots(figsize=(10, 6))
colors_workingday = ['#D3D3D3', '#90CAF9']
sns.barplot(data=workingday_avg, x='workingday',
            y='total_rentals', palette=colors_workingday, ax=ax3)
ax3.set_title('Rata-rata Peminjaman Sepeda: Hari Kerja vs Hari Libur',
              loc='center', fontsize=15)
ax3.set_xlabel('Jenis Hari', fontsize=12)
ax3.set_ylabel('Rata-rata Total Peminjaman', fontsize=12)
ax3.tick_params(axis='x', labelsize=12)
ax3.tick_params(axis='y', labelsize=12)
for container in ax3.containers:
    ax3.bar_label(container, fmt='%.0f', padding=3, fontsize=12)
plt.tight_layout()
st.pyplot(fig3)

st.markdown('---')

# =====================
# VISUALISASI 4 - Tren Bulanan
# =====================
st.subheader('Pertanyaan 4: Tren Total Peminjaman Sepeda per Bulan (2011 vs 2012)')

monthly_trend = df_filtered.groupby(['year', 'month'], observed=True)['total_rentals'].sum().reset_index()

fig4, ax4 = plt.subplots(figsize=(12, 6))
for yr, group in monthly_trend.groupby('year', observed=True):
    label = '2011' if yr == 0 else '2012'
    ax4.plot(group['month'], group['total_rentals'],
             marker='o', linewidth=2, markersize=8, label=label)
ax4.set_title('Tren Total Peminjaman Sepeda per Bulan (2011 vs 2012)',
              loc='center', fontsize=15)
ax4.set_xlabel('Bulan', fontsize=12)
ax4.set_ylabel('Total Peminjaman', fontsize=12)
ax4.set_xticks(range(1, 13))
ax4.set_xticklabels(['Jan','Feb','Mar','Apr','Mei','Jun',
                     'Jul','Agu','Sep','Okt','Nov','Des'], fontsize=11)
ax4.tick_params(axis='y', labelsize=11)
ax4.legend(title='Tahun', fontsize=11, title_fontsize=12)
plt.tight_layout()
st.pyplot(fig4)

st.markdown('---')

# =====================
# VISUALISASI 5 - Clustering Kategori Waktu
# =====================
st.subheader('Analisis Lanjutan: Rata-rata Peminjaman Berdasarkan Kategori Waktu')

bins_hour = [0, 6, 11, 15, 19, 23]
labels_hour = ['Dini Hari', 'Pagi', 'Siang', 'Sore', 'Malam']
df_hour_filtered['time_of_day'] = pd.cut(df_hour_filtered['hour'],
                                          bins=bins_hour,
                                          labels=labels_hour,
                                          include_lowest=True)
time_avg = df_hour_filtered.groupby('time_of_day', observed=True)['total_rentals'].mean().reset_index()

fig5, ax5 = plt.subplots(figsize=(10, 6))
colors_time = ['#D3D3D3', '#90CAF9', '#90CAF9', '#66BB6A', '#D3D3D3']
sns.barplot(data=time_avg, x='time_of_day',
            y='total_rentals', palette=colors_time, ax=ax5)
ax5.set_title('Rata-rata Peminjaman Berdasarkan Kategori Waktu',
              loc='center', fontsize=15)
ax5.set_xlabel('Kategori Waktu', fontsize=12)
ax5.set_ylabel('Rata-rata Total Peminjaman', fontsize=12)
ax5.tick_params(axis='x', labelsize=12)
ax5.tick_params(axis='y', labelsize=12)
for container in ax5.containers:
    ax5.bar_label(container, fmt='%.0f', padding=3, fontsize=12)
plt.tight_layout()
st.pyplot(fig5)

st.caption('Copyright © Bike Sharing Dashboard 2024')

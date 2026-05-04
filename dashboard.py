import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# LOAD DATA

df_day = pd.read_csv('day_clean.csv')
df_hour = pd.read_csv('hour_clean.csv')


# JUDUL DASHBOARD

st.title('Bike Sharing Dashboard 2011-2012')
st.markdown('Analisis data peminjaman sepeda periode 2011-2012')


# OVERVIEW

st.subheader('Overview')
col1, col2, col3 = st.columns(3)
with col1:
    st.metric('Total Peminjaman', f"{df_day['total_rentals'].sum():,}")
with col2:
    st.metric('Rata-rata Harian', f"{df_day['total_rentals'].mean():.0f}")
with col3:
    st.metric('Hari Tertinggi', f"{df_day['total_rentals'].max():,}")

st.markdown('---')


# VISUALISASI 1 - Hari Kerja vs Libur

st.subheader('Rata-rata Peminjaman: Hari Kerja vs Hari Libur')

workingday_avg = df_day.groupby('workingday')['total_rentals'].mean().reset_index()
workingday_avg['workingday'] = workingday_avg['workingday'].map({
    0: 'Hari Libur', 
    1: 'Hari Kerja'
})

fig1, ax1 = plt.subplots(figsize=(10, 6))
colors1 = ['#D3D3D3', '#90CAF9']
sns.barplot(data=workingday_avg, x='workingday', 
            y='total_rentals', palette=colors1, ax=ax1)
ax1.set_title('Rata-rata Peminjaman: Hari Kerja vs Hari Libur', 
              loc='center', fontsize=15)
ax1.set_xlabel('Jenis Hari', fontsize=12)
ax1.set_ylabel('Rata-rata Total Peminjaman', fontsize=12)
ax1.tick_params(axis='x', labelsize=12)
ax1.tick_params(axis='y', labelsize=12)
for container in ax1.containers:
    ax1.bar_label(container, fmt='%.0f', padding=3, fontsize=12)
plt.tight_layout()
st.pyplot(fig1)

st.markdown('---')


# VISUALISASI 2 - Tren Bulanan

st.subheader('Tren Total Peminjaman Sepeda per Bulan (2011 vs 2012)')

df_day['date'] = pd.to_datetime(df_day['date'])
monthly_trend = df_day.groupby(['year', 'month'])['total_rentals'].sum().reset_index()

fig2, ax2 = plt.subplots(figsize=(12, 6))
for yr, group in monthly_trend.groupby('year'):
    label = '2011' if yr == 0 else '2012'
    ax2.plot(group['month'], group['total_rentals'],
             marker='o', linewidth=2, markersize=8, label=label)
ax2.set_title('Tren Total Peminjaman Sepeda per Bulan (2011 vs 2012)', 
              loc='center', fontsize=15)
ax2.set_xlabel('Bulan', fontsize=12)
ax2.set_ylabel('Total Peminjaman', fontsize=12)
ax2.set_xticks(range(1, 13))
ax2.set_xticklabels(['Jan','Feb','Mar','Apr','Mei','Jun',
                     'Jul','Agu','Sep','Okt','Nov','Des'], fontsize=11)
ax2.tick_params(axis='y', labelsize=11)
ax2.legend(title='Tahun', fontsize=11, title_fontsize=12)
plt.tight_layout()
st.pyplot(fig2)

st.markdown('---')


# VISUALISASI 3 - Clustering Kategori Waktu

st.subheader('Rata-rata Peminjaman Berdasarkan Kategori Waktu')

bins_hour = [0, 6, 11, 15, 19, 23]
labels_hour = ['Dini Hari', 'Pagi', 'Siang', 'Sore', 'Malam']
df_hour['time_of_day'] = pd.cut(df_hour['hour'],
                                bins=bins_hour,
                                labels=labels_hour,
                                include_lowest=True)
time_avg = df_hour.groupby('time_of_day', observed=True)['total_rentals'].mean().reset_index()

fig3, ax3 = plt.subplots(figsize=(10, 6))
colors3 = ['#D3D3D3', '#90CAF9', '#90CAF9', '#90CAF9', '#D3D3D3']
sns.barplot(data=time_avg, x='time_of_day',
            y='total_rentals', palette=colors3, ax=ax3)
ax3.set_title('Rata-rata Peminjaman Berdasarkan Kategori Waktu', 
              loc='center', fontsize=15)
ax3.set_xlabel('Kategori Waktu', fontsize=12)
ax3.set_ylabel('Rata-rata Total Peminjaman', fontsize=12)
ax3.tick_params(axis='x', labelsize=12)
ax3.tick_params(axis='y', labelsize=12)
for container in ax3.containers:
    ax3.bar_label(container, fmt='%.0f', padding=3, fontsize=12)
plt.tight_layout()
st.pyplot(fig3)

st.caption('Copyright © Bike Sharing Dashboard 2024')
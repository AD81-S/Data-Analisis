# install library
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import textwrap 
from matplotlib.ticker import FuncFormatter
sns.set(style='dark')

def wrap_labels(labels, width):
    return ['\n'.join(textwrap.wrap(label, width)) for label in labels]

def create_Cuaca_Mendukung(df): # Buat Fungsi create_Cuaca_mendukung
    Cuaca_Mendukung_df = df.groupby(by='weathersit_x').agg({
        'cnt_x': 'sum'
        })
    Cuaca_Mendukung_df = Cuaca_Mendukung_df.reset_index()
    Cuaca_Mendukung_df.rename(columns={
        "weathersit_x": "Cuaca",
        "cnt_x": "Total_Sewa"
    }, inplace=True)
    return Cuaca_Mendukung_df

def create_Musim_Mendukung(df): # Buat Fungsi create_Cuaca_mendukung
    Musim_Mendukung_df = df.groupby(by='season_x').agg({
        'cnt_x': 'sum'
        })
    Musim_Mendukung_df = Musim_Mendukung_df.reset_index()
    Musim_Mendukung_df.rename(columns={
        "season_x": "Musim",
        "cnt_x": "Total_Sewa"
    }, inplace=True)
    return Musim_Mendukung_df

All_df = pd.read_csv("All_data.csv") # Simpan All_data.csv --> All_df

# filter fungsi yang sudah dibuat
Cuaca_Mendukung_df = create_Cuaca_Mendukung(All_df) 
Musim_Mendukung_df = create_Musim_Mendukung(All_df)

st.title("Cuaca dan Musim Analysis")

# Musim
st.header("Analisis Sewa Sepeda Setiap Musim")
musim_counts = Musim_Mendukung_df['Musim'].value_counts()
fig1, ax1 = plt.subplots()
ax1.pie(musim_counts, labels=musim_counts.index, autopct='%1.1f%%', startangle=90)
ax1.axis('equal') 
st.pyplot(fig1)


# Cuaca
st.header("Analisis Sewa Sepeda Setiap Cuaca")
cuaca_counts = Cuaca_Mendukung_df.groupby('Cuaca')['Total_Sewa'].sum()
fig2, ax2 = plt.subplots()
cuaca_counts.plot(kind='bar', ax=ax2, color='skyblue')

wrapped_labels = wrap_labels(cuaca_counts.index, 10)
ax2.set_xticklabels(wrapped_labels, rotation=0, ha='right')

ax2.set_title('Jumlah Sewa Berdasarkan Cuaca')
ax2.set_xlabel('Cuaca')
ax2.set_ylabel('Total Sewa')
ax2.grid(axis='y', linestyle='--', alpha=0.7)

ax2.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))

plt.tight_layout()
st.pyplot(fig2)
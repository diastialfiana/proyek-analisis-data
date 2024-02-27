import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style seaborn
sns.set(style='dark')

# Load data
df_day = pd.read_csv("https://raw.githubusercontent.com/diastialfiana/proyek-analisis-data/main/day.csv")
df_day['dteday'] = pd.to_datetime(df_day['dteday'])

# Rename columns and map numerical values to descriptive labels
df_day.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'hr': 'hour',
    'weathersit': 'weather_cond',
    'cnt': 'count'
}, inplace=True)

df_day['month'] = df_day['month'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})
df_day['season'] = df_day['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})
df_day['weekday'] = df_day['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
})
df_day['weather_cond'] = df_day['weather_cond'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Heavy Rain/Thunderstrom'
})

# Sidebar - Date Range Selection
min_date = pd.to_datetime(df_day['dateday']).dt.date.min()
max_date = pd.to_datetime(df_day['dateday']).dt.date.max()

with st.sidebar:
    st.image('https://image.shutterstock.com/image-vector/bicycle-rental-service-guy-rents-260nw-2286786925.jpg', use_column_width=True)
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data based on selected date range
main_df = df_day[(df_day['dateday'] >= str(start_date)) & (df_day['dateday'] <= str(end_date))]

# Dashboard
st.header('Bike Rental Center')

# Daily Rentals Metrics
st.subheader('Daily Rentals')
col1, col2, col3 = st.columns(3)

with col1:
    st.metric('Pengguna Casual', value=main_df['casual'].sum())

with col2:
    st.metric('Pengguna Registered', value=main_df['registered'].sum())

with col3:
    st.metric('Jumlah Total Pengguna', value=main_df['count'].sum())

# Weekday, Workingday, and Holiday Rentals
st.subheader('Weekday, Workingday, and Holiday Rentals')

fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(15, 10))

# Weekday Rentals
sns.barplot(x='weekday', y='count', data=main_df.groupby('weekday')['count'].sum().reset_index(), palette="viridis", ax=axes[0])
axes[0].set_title('Jumlah Penyewa Berdasarkan Weekday')

# Workingday Rentals
sns.barplot(x='workingday', y='count', data=main_df.groupby('workingday')['count'].sum().reset_index(), palette="viridis", ax=axes[1])
axes[1].set_title('Jumlah Penyewa berdasarkan Hari Kerja')

# Holiday Rentals
sns.barplot(x='holiday', y='count', data=main_df.groupby('holiday')['count'].sum().reset_index(), palette="viridis", ax=axes[2])
axes[2].set_title('Number of Rents based on Holiday')

for ax in axes:
    ax.set_ylabel(None)
    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=10)
    for index, row in enumerate(ax.patches):
        ax.text(index, row.get_height() + 1, str(int(row.get_height())), ha='center', va='bottom', fontsize=10)

plt.tight_layout()
st.pyplot(fig)

# Monthly Rentals based on Season and Year
st.subheader('Jumlah total sepeda yang disewakan berdasarkan Bulan dan tahun')
fig, ax = plt.subplots(figsize=(16, 8))

monthly_counts = main_df.groupby(["month", "year"]).agg({"count": "sum"}).reset_index()

sns.lineplot(
    data=monthly_counts,
    x="month",
    y="count",
    hue="year",
    palette="rocket",
    marker="o")

ax.set_title('Jumlah total sepeda yang disewakan berdasarkan Bulan dan tahun')
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)

ax.legend(title="Tahun", loc="upper right")
plt.tight_layout()
st.pyplot(fig)

# Relationship between Windspeed and Registered Users
st.subheader('Hubungan Kecepatan Angin dengan Jumlah Pengguna Terdaftar')
fig, ax = plt.subplots(figsize=(16, 8))

sns.scatterplot(
    data=main_df,
    x="windspeed",
    y="registered",
    palette="rocket",
    marker="o")

ax.set_title('Hubungan Kecepatan Angin dengan Jumlah Pengguna Terdaftar')
ax.set_ylabel('Total Pengguna Terdaftar')
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)

plt.tight_layout()
st.pyplot(fig)

# Registered Users on Working Days
st.subheader('Jumlah Sewa Sepeda Teregistrasi pada Hari Kerja')
fig, ax = plt.subplots(figsize=(16, 8))

filtered_data = main_df[(main_df["workingday"] == 1) & (main_df["registered"] > 0)]

sns.barplot(
    data=filtered_data,
    x="weekday",
    y="registered")

ax.set_title('Jumlah Sewa Sepeda Teregistrasi pada Hari Kerja')
ax.set_ylabel('Total Pengguna Terdaftar')
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)

plt.tight_layout()
st.pyplot(fig)

# Total Bike Users based on Time of Day
st.subheader('Jumlah Pengguna Sepeda berdasarkan waktu Hari')
fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(
    x='weekday',
    y='count',
    data=main_df)

ax.set_title('Jumlah Pengguna Sepeda berdasarkan waktu Hari')
ax.set_xlabel('Waktu/Jam')
ax.set_ylabel('Jumlah Pengguna Sepeda')
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)

plt.tight_layout()
st.pyplot(fig)

# Seasonal Rentals based on Season and Year
st.subheader('Jumlah total sepeda yang disewakan berdasarkan Musim dan tahun')
fig, ax = plt.subplots(figsize=(16, 8))

season_counts = main_df.groupby(by=["season", "year"]).agg({"count": "sum"}).reset_index()

sns.lineplot(
    data=season_counts,
    x="season",
    y="count",
    hue="year",
    palette="rocket",
    marker="o")

ax.set_title('Jumlah total sepeda yang disewakan berdasarkan Musim dan tahun')
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)

plt.tight_layout()
st.pyplot(fig)

# Dashboard Footer
st.caption('Made By Diasti Alfiana/Dicoding 2024')

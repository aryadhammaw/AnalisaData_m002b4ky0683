import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

#read the csv data
dfDay = pd.read_csv('day.csv')
dfHour = pd.read_csv('hour.csv')

#convert the date type
dfDay['dteday'] = pd.to_datetime(dfDay['dteday'])
dfHour['dteday'] = pd.to_datetime(dfHour['dteday'])

#define min_date and max_date
min_date = dfHour["dteday"].min()
max_date = dfHour["dteday"].max()


#meminta input dari user
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("logo_itb.png")
    
    # Mengambil tanggal dari user
    selected_date = st.date_input(
        label='Choose Date',min_value=min_date,
        max_value=max_date,
        value=min_date
    )

#proses input dari user, pilih data yang hanya diminta user
filtered_df_hour = dfHour[dfHour['dteday'] == pd.to_datetime(selected_date)]
filtered_df_day = dfDay[dfDay['dteday'] == pd.to_datetime(selected_date)]

st.header('Proyek Dicoding Analisa Data[Bike Sharing Dataset]')
st.subheader('Bike User Information for the Selected Date (hourly)')

fig, ax = plt.subplots(figsize=(16, 8))

# Create a bar plot 
ax.bar(
    dfHour[dfHour['dteday'] == pd.to_datetime(selected_date)]["hr"],
    dfHour[dfHour['dteday'] == pd.to_datetime(selected_date)]["cnt"],
    color="#90CAF9"
)

# Set tick parameters for better readability
ax.set_ylabel('Number of bike users', fontsize = 30)
ax.set_xlabel("Time", fontsize=30)
ax.set_title("Hourly Bike User Information for a Day", loc="center", fontsize=50)

ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

# Display the plot in Streamlit
st.pyplot(fig)

st.subheader('Bike User Information for the Selected Date (Daily)')

# Create a new figure and axis for the plot
fig, ax = plt.subplots(figsize=(10, 6))


# Aggregating the total number of users per category for the selected date
total_registered = dfDay[dfDay['dteday'] == pd.to_datetime(selected_date)]['registered']
total_casual = dfDay[dfDay['dteday'] == pd.to_datetime(selected_date)]['casual']

# Bar width to control spacing between bars
bar_width = 0.4

# X positions for the bars (since there's only one date, we use a dummy value for positioning)
x_pos = [0]

# Create a bar for 'registered' users
ax.bar(
    [p - bar_width/2 for p in x_pos],  # Shift to the left
    total_registered,
    width=bar_width,
    color="#90CAF9",
    label="Registered"
)

# Create a bar for 'casual' users
ax.bar(
    [p + bar_width/2 for p in x_pos],  # Shift to the right
    total_casual,
    width=bar_width,
    color="#FFA726",
    label="Casual"
)

# Set tick parameters for better readability
ax.set_ylabel('Number of Bike Users', fontsize=20)
ax.set_title(f"Comparison of Bike Users on {selected_date}", fontsize=25)

# Set x-axis label to show the date
ax.set_xticks(x_pos)
ax.set_xticklabels([selected_date.strftime('%Y-%m-%d')], fontsize=15)

# Add a legend to differentiate between registered and casual users
ax.legend(fontsize=15)

# Display the plot in Streamlit
st.pyplot(fig)

st.caption('Copyright (c) Aryadharma Wibowo m002b4ky0683@bangkit.academy')
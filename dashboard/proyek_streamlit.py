import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import matplotlib.lines as mlines

# Read the csv data
dfDay = pd.read_csv('data/day.csv')
dfHour = pd.read_csv('data/hour.csv')

# Convert the date type
dfDay['dteday'] = pd.to_datetime(dfDay['dteday'])
dfHour['dteday'] = pd.to_datetime(dfHour['dteday'])

# Define min_date and max_date
min_date = dfHour["dteday"].min()
max_date = dfHour["dteday"].max()

# Request input from the user
with st.sidebar:
    # Display the company logo
    st.image("data/logo_bangkit.jpg")
    
    # Get start_date & end_date from date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data based on user input
filtered_df_hour = dfHour[(dfHour["dteday"] >= pd.to_datetime(start_date)) & (dfHour["dteday"] <= pd.to_datetime(end_date))]
filtered_df_day = dfDay[(dfDay["dteday"] >= pd.to_datetime(start_date)) & (dfDay["dteday"] <= pd.to_datetime(end_date))]

st.header('Proyek Dicoding Analisa Data [Bike Sharing Dataset]')
st.write('for more analysis, check my code on colab: https://drive.google.com/file/d/1tOcfvM-OdNYXkPSziKBqsODkIzzxthBT/view?usp=sharing')
st.subheader('Which times of day experience the highest bike users ("cnt") across selected start and end date?')
st.write('Select the date provided from left corner of your screen')

# Filter data by seasons
filtered_dfHour_Spring = filtered_df_hour[filtered_df_hour['season'] == 2]
filtered_dfHour_Summer = filtered_df_hour[filtered_df_hour['season'] == 3]
filtered_dfHour_Fall = filtered_df_hour[filtered_df_hour['season'] == 4]
filtered_dfHour_Winter = filtered_df_hour[filtered_df_hour['season'] == 1]

# Calculate quantiles for high demand hours
filtered_dfHour_Spring_Q3 = filtered_dfHour_Spring['cnt'].quantile(0.75)
filtered_dfHour_Summer_Q3 = filtered_dfHour_Summer['cnt'].quantile(0.75)
filtered_dfHour_Fall_Q3 = filtered_dfHour_Fall['cnt'].quantile(0.75)
filtered_dfHour_Winter_Q3 = filtered_dfHour_Winter['cnt'].quantile(0.75)

filtered_Hdemand_Hourly_Spring = filtered_dfHour_Spring[filtered_dfHour_Spring['cnt'] >= filtered_dfHour_Spring_Q3]
filtered_Hdemand_Hourly_Summer = filtered_dfHour_Summer[filtered_dfHour_Summer['cnt'] >= filtered_dfHour_Summer_Q3]
filtered_Hdemand_Hourly_Fall = filtered_dfHour_Fall[filtered_dfHour_Fall['cnt'] >= filtered_dfHour_Fall_Q3]
filtered_Hdemand_Hourly_Winter = filtered_dfHour_Winter[filtered_dfHour_Winter['cnt'] >= filtered_dfHour_Winter_Q3]

# Calculate hourly demand for each season
time_count_Spring = {}
time_count_Summer = {}
time_count_Fall = {}
time_count_Winter = {}
for i in range(24):
    time_count_Spring[f'time {i}'] = (filtered_Hdemand_Hourly_Spring['hr'] == i).sum()
    time_count_Summer[f'time {i}'] = (filtered_Hdemand_Hourly_Summer['hr'] == i).sum()
    time_count_Fall[f'time {i}'] = (filtered_Hdemand_Hourly_Fall['hr'] == i).sum()
    time_count_Winter[f'time {i}'] = (filtered_Hdemand_Hourly_Winter['hr'] == i).sum()

# Plot grouped bar chart for each season
fig, ax = plt.subplots(figsize=(20, 6))

# Bar width
bar_width = 0.2
n = len(time_count_Spring)  # Number of time slots
x = np.arange(n)  # Positions for the bars

# Plot bars for each season
ax.bar(x, list(time_count_Winter.values()), width=bar_width, label='Winter', color='blue')
ax.bar(x + bar_width, list(time_count_Spring.values()), width=bar_width, label='Spring', color='orange')
ax.bar(x + 2 * bar_width, list(time_count_Summer.values()), width=bar_width, label='Summer', color='green')
ax.bar(x + 3 * bar_width, list(time_count_Fall.values()), width=bar_width, label='Fall', color='red')

# Add labels and title
ax.set_xlabel('Time', fontsize=15)
ax.set_ylabel('Count', fontsize=15)
ax.set_title(f'The hour with the highest peak count of bike users from date {start_date} until {end_date}', fontsize=20)

# Set x-axis ticks
ax.set_xticks(x + 1.5 * bar_width)
ax.set_xticklabels(list(time_count_Spring.keys()))

# Add a legend
ax.legend()

# Display the plot in Streamlit
st.pyplot(fig)

#number1 static results
st.write('Try to select the earliest and latest starting dates to see if you get the same results as shown in the graph below.')
st.image('data/number1_result.png')


##number 2 part 1
st.subheader('How does weather status ("weathersit") influence the number of bike rentals? (result part 1: scatter plot)')
# Create a figure and axis
fig, ax = plt.subplots(figsize=(10, 6))

# Define the discrete colormap for the different weather conditions
colors = ['#006400', '#FFD700', '#FF8C00']  # Green, Yellow, and Orange for 3 weather categories
weather_labels = ['Good Weather', 'Moderate Weather', 'Bad Weather']  # Example labels

# Map weather status to color
weather_status_colors = {1: '#006400', 2: '#FFD700', 3: '#FF8C00'}
weather_status_legend = {1: 'Good Weather', 2: 'Moderate Weather', 3: 'Bad Weather'}

# Scatter plot: X-axis as 'dteday', Y-axis as 'cnt', color determined by 'weathersit'
for weathersit, color in weather_status_colors.items():
    # Plot each weather status separately to ensure legend is fixed
    data_subset = filtered_df_day[filtered_df_day['weathersit'] == weathersit]
    ax.scatter(data_subset['dteday'], data_subset['cnt'], color=color, label=weather_status_legend[weathersit], alpha=0.6)

# Create a custom legend (whether or not certain statuses are in the filtered data)
good_weather = mlines.Line2D([], [], color='#006400', marker='o', linestyle='None', markersize=10, label='Good Weather')
moderate_weather = mlines.Line2D([], [], color='#FFD700', marker='o', linestyle='None', markersize=10, label='Moderate Weather')
bad_weather = mlines.Line2D([], [], color='#FF8C00', marker='o', linestyle='None', markersize=10, label='Bad Weather')

# Add the fixed legend
ax.legend(handles=[good_weather, moderate_weather, bad_weather])

# Add labels and title
ax.set_xlabel('Date')
ax.set_ylabel('Bike Users')
ax.set_title(f'Count by Weather Status and Days from {start_date} until {end_date}')

# Show the plot in Streamlit
st.pyplot(fig)

#number 2 part 1 static result
st.write('Try to select the earliest and latest starting dates to see if you get the same results as shown in the graph below.')
st.image('data/number2_1_result.png')

st.subheader('How does weather status ("weathersit") influence the number of bike rentals? (result part 2)')
#number 2 part 2
# Group data by weather condition and calculate the average rentals
weather_groups = filtered_df_day.groupby('weathersit')['cnt'].mean()

# Bar plot of average bike rentals per weather condition
colors = ['#006400', '#FFD700', '#FF8C00', '#FF0000']  # Add a color for 4th weather category if needed
fig, ax = plt.subplots()

weather_groups.plot(kind='bar', color=colors, ax=ax)
ax.set_xlabel(
    'Weather Condition:\n'
    '1: Clear, Few clouds, Partly cloudy\n'
    '2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist\n'
    '3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds\n'
    '4: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog'
)
ax.set_ylabel('Average Bike Users')
ax.set_title(f'Average Bike Users Across Different Weather Conditions from {start_date} until {end_date}')

# Display the plot in Streamlit
st.pyplot(fig)

#number 2 part 2 static result
st.write('Try to select the earliest and latest starting dates to see if you get the same results as shown in the graph below.')
st.image('data/number2_2_result.png')

st.title("Conclusion")

# Numbered List
st.markdown("### 1. Which times of day experience the highest bike rental demand across different seasons?\n")
st.write("Answer: time 17 and 18 are consistently being the peak hour for bike users across the seasons")
st.markdown("### 2. How does weather condition (e.g., clear vs. rainy days) influence the number of bike rentals?")
st.markdown("answer 2.1: ")
st.write(
    "There is a low negative correlation of -0.3225 between the weather status and the number of bike users across the seasons. "
    "However, this correlation is statistically significant, with a p-value of approximately $3.11 \\times 10^{-17}$."
)
st.markdown("answer 2.2")
st.write("if we just consider spring season, the correlation is quite moderate, which is in ≈ -0.49")
            

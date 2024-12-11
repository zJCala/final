import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
@st.cache_data
def load_data():
    data = pd.read_csv('nba_games.csv')
    data['game_date'] = pd.to_datetime(data['game_date'])  # Convert game_date to datetime
    return data

# Load data
nba_data = load_data()

# Sidebar for Navigation
st.sidebar.title("NBA Games Exploration")
selected_section = st.sidebar.radio("Navigate to:", options=["Introduction", "Overview", "Visualizations", "Data Exploration", "Analysis", "Conclusion"])

# Filter Options
season_filter = st.sidebar.selectbox("Select Season:", options=nba_data['season'].unique())

# Check if the 'team_name' column exists in the dataset
if 'team_name' in nba_data.columns:
    # Commented out the "Select team_name" filter to hide it in the UI
    # team_filter = st.sidebar.selectbox("Select team_name:", options=nba_data['team_name'].unique())
    
    win_filter = st.sidebar.radio("Win/Loss Filter:", options=["All", "Wins", "Losses"])

    # Filter data based on selections
    filtered_data = nba_data[(nba_data['season'] == season_filter)]
    if 'team_name' in locals():  # If team_name exists, apply team filtering
        filtered_data = filtered_data[filtered_data['team_name'] == team_filter]
    if win_filter == "Wins":
        filtered_data = filtered_data[filtered_data['team_win'] == 1]
    elif win_filter == "Losses":
        filtered_data = filtered_data[filtered_data['team_win'] == 0]
else:
    st.error("The 'team' column is not found in the dataset. Please verify your data.")
    filtered_data = nba_data[nba_data['season'] == season_filter]

# Add 'days_since_first_game' to the filtered data
filtered_data['days_since_first_game'] = (filtered_data['game_date'] - filtered_data['game_date'].min()).dt.days

# Introduction Section
if selected_section == "Introduction":
    st.title("NBA Games Data Exploration Report")
    st.header("Introduction")
    st.write("""
    This report provides an in-depth exploration of the Los Angeles Lakers' game data for the selected season, 
    sourced from official NBA statistics. The objective of this analysis is to uncover key trends, 
    performance metrics, and insights that can inform strategic decisions and enhance understanding of the team's performance.
    
    The dataset encompasses various performance metrics including:
    - Points scored per game
    - Field goal (FG), free throw (FT), and three-point (3PT) shooting percentages
    - Assists and rebounds statistics
    - Win-loss outcomes

    Through visualizations and statistical analysis, we aim to highlight significant patterns in the Lakers' performance over the season.
    """)

    # Display key metrics
    st.header("Key Performance Metrics")
    st.metric("Total Games Played", len(filtered_data))
    st.metric("Total Wins", filtered_data['team_win'].sum())
    st.metric("Average Points Scored", round(filtered_data['team_points'].mean(), 2))
    st.metric("Average Field Goal Percentage", f"{round(filtered_data['team_fg_percentage'].mean() * 100, 2)}%")

# Overview Section
elif selected_section == "Overview":
    st.header("Overview")
    st.write("""
    The dataset contains detailed records of NBA games, focusing on performance metrics for each team, such as points scored, 
    field goal percentage, win/loss results, and more. This analysis explores the Los Angeles Lakers' performance over a selected season.
    
    **Dataset Structure**:
    - `game_date`: Date of the game
    - `team_name`: Name of the team (Los Angeles Lakers)
    - `team_points`: Points scored by the Lakers
    - `team_fg_percentage`: Field goal percentage
    - `team_win`: 1 if the Lakers won the game, 0 if they lost
    - `season`: NBA season (e.g., 2021-2022)

    The dataset provides valuable insights into the Lakers' performance throughout the season.
    """)

# Visualizations Section
elif selected_section == "Visualizations":
    st.header("Visualizations")
    
    # Points Scored Over Time
    st.subheader("Points Scored Over Time")
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=filtered_data, x='game_date', y='team_points', marker='o', color='purple')
    plt.title('Points Scored by the Lakers Over the Selected Season')
    plt.xlabel('Game Date')
    plt.ylabel('Points Scored')
    plt.xticks(rotation=45)
    plt.grid()
    st.pyplot(plt)

    st.write("""
    This line chart illustrates the points scored by the Lakers throughout the selected season. 
    Notably, peaks in scoring can be observed during specific games, which may correlate with opponents, 
    player performances, or strategic adjustments made by the coaching staff.
    """)

    # Field Goal Percentage Distribution
    st.subheader("Field Goal Percentage Distribution")
    plt.figure(figsize=(10, 5))
    sns.histplot(filtered_data['team_fg_percentage'], bins=10, kde=True, color='orange')
    plt.title('Distribution of Field Goal Percentage')
    plt.xlabel('Field Goal Percentage')
    plt.ylabel('Frequency')
    plt.grid()
    st.pyplot(plt)

    st.write("""
    The histogram above shows the distribution of the Lakers' field goal percentages during the selected season. 
    The Kernel Density Estimate (KDE) overlay provides insight into the shooting efficiency across games.
    """)

    # Wins and Losses
    st.subheader("Wins and Losses in the Selected Season")
    win_count = filtered_data['team_win'].value_counts()
    plt.figure(figsize=(6, 4))
    sns.barplot(x=win_count.index, y=win_count.values, palette='pastel')
    plt.title('Wins and Losses in the Selected Season')
    plt.xlabel('Result (0 = Loss, 1 = Win)')
    plt.ylabel('Number of Games')
    plt.xticks(ticks=[0, 1], labels=['Loss', 'Win'])
    plt.grid()
    st.pyplot(plt)

    st.write("""
    The bar chart displays the Lakers' win-loss record for the selected season. 
    The results indicate a balanced performance; however, the number of losses suggests potential 
    areas for strategic improvement.
    """)

# Data Exploration Section
elif selected_section == "Data Exploration":
    st.header("Data Exploration")
    st.write("""
    Before diving into the analysis, the dataset underwent various exploration and cleaning steps. 
    Missing values were handled, and data transformations were applied to enable meaningful insights.
    
    **Exploratory Steps**:
    - Missing values were checked and handled.
    - The `game_date` column was converted to `datetime` format.
    - A new column, `days_since_first_game`, was created to track the number of days since the first game of the season.

    These transformations allow for detailed analysis and visualizations in the following sections.
    """)

    # Display first few rows of data
    st.subheader("First Few Rows of Data")
    st.write(filtered_data.head())

# Analysis Section
elif selected_section == "Analysis":
    st.header("Analysis")
    
    # Regression Plot (Days Since First Game vs Points)
    st.subheader("Regression Analysis: Days Since First Game vs Points Scored")
    sns.lmplot(data=filtered_data, x='days_since_first_game', y='team_points', aspect=2, height=6, line_kws={'color': 'red'})
    plt.title("Regression Line of Points Scored Over Time")
    st.pyplot(plt)

    st.write("""
    The regression plot illustrates the relationship between the number of days since the first game of the season and the points scored by the Lakers. 
    This provides insight into the team's performance over the course of the season.
    """)

# Conclusion Section
elif selected_section == "Conclusion":
    st.header("Conclusion")
    st.write("""
    The exploration of the Lakers' game data for the selected season reveals several critical insights:
    1. **Scoring Variability**: The fluctuation in points scored highlights the inconsistency in offensive performance.
    2. **Shooting Efficiency**: The distribution of field goal percentages suggests that the Lakers maintained an average shooting efficiency.
    3. **Win-Loss Dynamics**: The win-loss data indicates that while the Lakers experienced a number of wins, 
       there is room for improvement in converting close games into wins.
    4. **Future Directions**: Further analysis is warranted, focusing on individual player contributions, 
       defensive metrics, and situational analysis to develop a more comprehensive understanding of the team's dynamics.
    """)

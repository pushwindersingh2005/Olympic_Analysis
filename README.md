# Olympic Analysis Web App (Streamlit + Pandas + Plotly)

import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import plotly.figure_factory as ff
import seaborn as sns
import matplotlib.pyplot as plt

# ----------------------------
# Load Data
# ----------------------------
df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

# Merge region info into main DataFrame
df = df.merge(region_df[['NOC', 'region']], on='NOC', how='left')

# Apply preprocessing
df = preprocessor.preprocess()

# ----------------------------
# Sidebar Menu
# ----------------------------
st.sidebar.title('🏅 Olympic Analysis')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis')
)

# ----------------------------
# Medal Tally Section
# ----------------------------
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    # Dynamic Titles
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("🏆 Overall Medal Tally")
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.title(f"🏅 Medal Tally in {selected_year} Olympics")
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.title(f"🌍 {selected_country} - Overall Performance")
    else:
        st.title(f"🥇 {selected_country} Performance in {selected_year} Olympics")

    st.table(medal_tally)

# ----------------------------
# Overall Analysis Section
# ----------------------------
if user_menu == 'Overall Analysis':
    # Top Stats
    editions = df['Year'].nunique() - 1
    cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = df['Name'].nunique()
    nations = df['region'].nunique()

    st.title("📊 Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions"); st.title(editions)
    with col2:
        st.header("Hosts"); st.title(cities)
    with col3:
        st.header("Sports"); st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events"); st.title(events)
    with col2:
        st.header("Athletes"); st.title(athletes)
    with col3:
        st.header("Nations"); st.title(nations)

    # Nations Over Time
    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x='Year', y='count', markers=True)
    st.title("🌍 Nations Over the Years")
    st.plotly_chart(fig)

    # Events Over Time
    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x='Year', y='count', markers=True)
    st.title("🎉 Events Over the Years")
    st.plotly_chart(fig)

    # Athletes Over Time
    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x='Year', y='count', markers=True)
    st.title("👨‍🦱 Athletes Over the Years")
    st.plotly_chart(fig)

    # Heatmap of Sports vs Years
    st.title("🔥 Number of Events per Sport Over Time")
    fig, ax = plt.subplots(figsize=(15, 10))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    sns.heatmap(
        x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int),
        annot=True, ax=ax
    )
    st.pyplot(fig)

# ----------------------------
# Country-wise Analysis Section
# ----------------------------
if user_menu == 'Country-wise Analysis':
    st.title("🌎 Country-wise Analysis")

# ----------------------------
# Athlete-wise Analysis Section
# ----------------------------
if user_menu == 'Athlete wise Analysis':
    st.title("🏃 Athlete-wise Analysis")

    # Age Distribution
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot(
        [x1, x2, x3, x4],
        ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
        show_hist=False, show_rug=False
    )
    st.title("📈 Distribution of Age")
    st.plotly_chart(fig)

    # Top 50 Sports
    st.title("⚡ Top 50 Sports")
    top_sports = df['Sport'].value_counts().head(50)
    st.bar_chart(top_sports)

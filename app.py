import streamlit as st
import pandas as pd
import plotly.express as px

st.title("COVID-19 Public Health Dashboard")

st.write(
    "Explore COVID-19 trends, country comparisons, geographical patterns, "
    "and relationships between public health indicators."
)

DATA_URL = "https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv"

selected_columns = [
    "country", "date", "code", "continent", "population",
    "total_cases", "new_cases", "total_cases_per_million",
    "new_cases_per_million", "total_deaths", "new_deaths",
    "total_deaths_per_million", "new_deaths_per_million",
    "population_density", "median_age", "life_expectancy",
    "gdp_per_capita", "hospital_beds_per_thousand"
]

remove_entities = [
    "Africa", "Asia", "Asia excl. China", "England",
    "England and Wales", "Europe", "European Union (27)",
    "High-income countries", "Low-income countries",
    "Lower-middle-income countries", "North America",
    "Northern Ireland", "Oceania", "Scotland", "South America",
    "Summer Olympics 2020", "Transnistria",
    "Upper-middle-income countries", "Wales",
    "Winter Olympics 2022", "World", "World excl. China",
    "World excl. China and South Korea",
    "World excl. China, South Korea, Japan and Singapore"
]

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    df = df[selected_columns]
    df = df[~df["country"].isin(remove_entities)]
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# Date range slider
start_date = df["date"].min().date()
end_date = df["date"].max().date()

date_range = st.slider(
    "Select Date Range",
    min_value=start_date,
    max_value=end_date,
    value=(start_date, end_date)
)

filtered_df = df[
    (df["date"] >= pd.Timestamp(date_range[0])) &
    (df["date"] <= pd.Timestamp(date_range[1]))
]

# Country comparison
countries = sorted(filtered_df["country"].unique())

selected_countries = st.multiselect(
    "Select Countries",
    countries,
    default=["India", "United States"]
)

comparison_df = filtered_df[
    filtered_df["country"].isin(selected_countries)
]

fig = px.line(
    comparison_df,
    x="date",
    y="total_cases",
    color="country",
    title="COVID-19 Total Cases Comparison"
)

st.plotly_chart(fig, use_container_width=True)

# Choropleth Map
latest_data = (
    filtered_df
    .sort_values("date")
    .groupby("country")
    .tail(1)
)

map_fig = px.choropleth(
    latest_data,
    locations="code",
    color="total_cases_per_million",
    hover_name="country",
    title="COVID-19 Cases per Million",
    color_continuous_scale="Reds"
)

st.plotly_chart(map_fig, use_container_width=True)

# Correlation Heatmap
correlation_data = df.groupby("country").agg({
    "total_cases_per_million": "max",
    "total_deaths_per_million": "max",
    "population": "max",
    "population_density": "max",
    "median_age": "max",
    "life_expectancy": "max",
    "gdp_per_capita": "max",
    "hospital_beds_per_thousand": "max"
})

correlation_matrix = correlation_data.corr()

st.subheader("Correlation Heatmap")

heatmap_fig = px.imshow(
    correlation_matrix,
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    zmin=-1,
    zmax=1,
    title="Correlation Heatmap"
)

st.plotly_chart(heatmap_fig, use_container_width=True)




    

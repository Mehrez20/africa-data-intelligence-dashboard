import pandas as pd
import panel as pn
import plotly.express as px
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest

pn.extension("plotly","tabulator")

# ----------------------------
# LOAD DATA
# ----------------------------

north_africa = pd.read_csv("data/north_africa_data.csv")

countries = sorted(north_africa["country"].unique())

# ----------------------------
# SELECTORS
# ----------------------------

country_select = pn.widgets.Select(
    name="Select Country",
    options=countries,
    value="Tunisia"
)

country_compare_1 = pn.widgets.Select(
    name="Country 1",
    options=countries,
    value="Tunisia"
)

country_compare_2 = pn.widgets.Select(
    name="Country 2",
    options=countries,
    value="Morocco"
)

year_slider = pn.widgets.IntSlider(
    name="Select Year",
    start=int(north_africa["year"].min()),
    end=int(north_africa["year"].max()),
    value=int(north_africa["year"].max()),
    step=1
)

# ----------------------------
# HEADER
# ----------------------------

header = pn.pane.Markdown(
"""
# 🌍 Africa Data Intelligence Dashboard
Interactive dashboard exploring **economy, population and environment data**
""",
styles={
"background":"#0f172a",
"color":"white",
"padding":"20px",
"border-radius":"10px"
}
)

# ----------------------------
# GET COUNTRY DATA
# ----------------------------

def get_country_data(country):
    return north_africa[north_africa["country"] == country]

# ----------------------------
# KPI
# ----------------------------

def kpi_dashboard(country):

    df = get_country_data(country)
    latest = df.iloc[-1]

    gdp = latest["gdp"]/1_000_000_000
    population = latest["population"]/1_000_000
    co2 = latest["co2"]

    kpi_gdp = pn.indicators.Number(
        name="GDP (Billion USD)",
        value=gdp,
        format="{value:.2f}",
        font_size="40pt"
    )

    kpi_pop = pn.indicators.Number(
        name="Population (Million)",
        value=population,
        format="{value:.2f}",
        font_size="40pt"
    )

    kpi_co2 = pn.indicators.Number(
        name="CO2 Emissions",
        value=co2,
        format="{value:.2f}",
        font_size="40pt"
    )

    return pn.Row(
        pn.Card(kpi_gdp,title="💰 Economy"),
        pn.Card(kpi_pop,title="👥 Population"),
        pn.Card(kpi_co2,title="🌿 Environment")
    )

kpi_row = pn.bind(kpi_dashboard,country_select)

# ----------------------------
# GDP CHART
# ----------------------------

def gdp_chart(country):

    df = get_country_data(country)

    fig = px.line(
        df,
        x="year",
        y="gdp",
        markers=True,
        title=f"{country} GDP Evolution"
    )

    return pn.pane.Plotly(fig,height=400)

gdp_plot = pn.bind(gdp_chart,country_select)

# ----------------------------
# UNEMPLOYMENT
# ----------------------------

def unemployment_chart(country):

    df = get_country_data(country)

    fig = px.line(
        df,
        x="year",
        y="unemployment",
        markers=True,
        title=f"{country} Unemployment Rate"
    )

    return pn.pane.Plotly(fig,height=400)

unemp_plot = pn.bind(unemployment_chart,country_select)

# ----------------------------
# SCATTER
# ----------------------------

def scatter_chart(country):

    df = get_country_data(country)

    fig = px.scatter(
        df,
        x="gdp",
        y="co2",
        size="population",
        color="year",
        title=f"{country} GDP vs CO2"
    )

    return pn.pane.Plotly(fig,height=500)

scatter_plot = pn.bind(scatter_chart,country_select)

# ----------------------------
# CORRELATION
# ----------------------------

def correlation_chart(country):

    df = get_country_data(country)

    corr = df.corr(numeric_only=True)

    fig = px.imshow(
        corr,
        text_auto=True,
        title=f"{country} Correlation Matrix"
    )

    return pn.pane.Plotly(fig,height=500)

corr_plot = pn.bind(correlation_chart,country_select)

# ----------------------------
# AFRICA MAP
# ----------------------------

def africa_map(year):

    df = north_africa[north_africa["year"]==year]

    fig = px.scatter_geo(
        df,
        lat="lat",
        lon="lon",
        size="gdp",
        color="gdp",
        hover_name="country",
        projection="natural earth",
        title=f"Africa Economic Map ({year})"
    )

    return pn.pane.Plotly(fig,height=500)

map_plot = pn.bind(africa_map,year_slider)

# ----------------------------
# ANIMATED MAP
# ----------------------------

def animated_map():

    fig = px.scatter_geo(
        north_africa,
        lat="lat",
        lon="lon",
        size="gdp",
        color="gdp",
        hover_name="country",
        animation_frame="year",
        projection="natural earth",
        title="Africa GDP Evolution"
    )

    return pn.pane.Plotly(fig,height=600)

# ----------------------------
# GDP RANKING
# ----------------------------

def top_gdp():

    latest = north_africa.groupby("country").last().reset_index()

    fig = px.bar(
        latest,
        x="country",
        y="gdp",
        color="country",
        title="Top GDP Countries"
    )

    return pn.pane.Plotly(fig,height=500)

# ----------------------------
# COUNTRY COMPARISON
# ----------------------------

def compare_countries(c1,c2):

    df = north_africa[north_africa["country"].isin([c1,c2])]

    fig = px.line(
        df,
        x="year",
        y="gdp",
        color="country",
        markers=True,
        title=f"GDP Comparison: {c1} vs {c2}"
    )

    return pn.pane.Plotly(fig,height=500)

compare_plot = pn.bind(compare_countries,country_compare_1,country_compare_2)

# ----------------------------
# CLUSTERING
# ----------------------------

def clustering():

    df = north_africa.copy()

    X = df[["gdp","population","co2"]]

    model = KMeans(n_clusters=3,n_init=10)

    df["cluster"] = model.fit_predict(X)

    fig = px.scatter(
        df,
        x="gdp",
        y="population",
        color="cluster",
        hover_name="country",
        title="Economic Clustering"
    )

    return pn.pane.Plotly(fig,height=500)

# ----------------------------
# ANOMALY DETECTION
# ----------------------------

def anomaly_detection():

    df = north_africa.copy()

    X = df[["gdp","population","co2"]]

    model = IsolationForest(contamination=0.05)

    df["anomaly"] = model.fit_predict(X)

    fig = px.scatter(
        df,
        x="gdp",
        y="population",
        color="anomaly",
        hover_name="country",
        title="Economic Anomaly Detection"
    )

    return pn.pane.Plotly(fig,height=500)

# ----------------------------
# AI PREDICTION
# ----------------------------

def prediction(country):

    df = get_country_data(country)

    X = df[["year"]]
    y = df["gdp"]

    model = LinearRegression()
    model.fit(X,y)

    future = np.arange(2024,2041).reshape(-1,1)

    pred = model.predict(future)

    pred_df = pd.DataFrame({
        "year":future.flatten(),
        "prediction":pred
    })

    fig = px.line(
        pred_df,
        x="year",
        y="prediction",
        title=f"{country} GDP Forecast (AI)"
    )

    return pn.pane.Plotly(fig,height=500)

prediction_plot = pn.bind(prediction,country_select)

# ----------------------------
# PAGES
# ----------------------------

overview_page = pn.Column(
    header,
    country_select,
    kpi_row,
    pn.Row(
        pn.Card(gdp_plot,title="GDP Evolution"),
        pn.Card(unemp_plot,title="Unemployment")
    )
)

viz_page = pn.Column(
    "# Visualization",
    scatter_plot
)

ds_page = pn.Column(
    "# Data Science",
    corr_plot
)

map_page = pn.Column(
    "# Africa Map",
    year_slider,
    map_plot
)

animated_map_page = pn.Column(
    "# Animated Map",
    animated_map()
)

ranking_page = pn.Column(
    "# GDP Ranking",
    top_gdp()
)

compare_page = pn.Column(
    "# Country Comparison",
    pn.Row(country_compare_1,country_compare_2),
    compare_plot
)

ml_page = pn.Column(
    "# Machine Learning",
    clustering()
)

anomaly_page = pn.Column(
    "# Anomaly Detection",
    anomaly_detection()
)

ai_page = pn.Column(
    "# AI Prediction",
    prediction_plot
)

table_page = pn.Column(
    "# Dataset",
    pn.widgets.Tabulator(north_africa,page_size=10)
)

# ----------------------------
# TABS
# ----------------------------

tabs = pn.Tabs(
    ("Overview",overview_page),
    ("Visualization",viz_page),
    ("Data Science",ds_page),
    ("Africa Map",map_page),
    ("Animated Map",animated_map_page),
    ("GDP Ranking",ranking_page),
    ("Comparison",compare_page),
    ("Machine Learning",ml_page),
    ("Anomaly Detection",anomaly_page),
    ("AI Prediction",ai_page),
    ("Dataset",table_page)
)

# ----------------------------
# TEMPLATE
# ----------------------------

template = pn.template.FastListTemplate(
    title="Africa Data Intelligence Dashboard",
    sidebar=[pn.pane.Markdown("## Navigation Dashboard")],
    main=[tabs],
    accent_base_color="#2563eb",
    header_background="#2563eb"
)

template.servable()
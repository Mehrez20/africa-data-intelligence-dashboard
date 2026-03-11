import pandas as pd
import panel as pn
import plotly.express as px

pn.extension("plotly")

# LOAD DATA
data = pd.read_csv("data/big_dataset.csv")

# latest data per country for map
latest = data.sort_values("year").groupby("country").last().reset_index()

# MAP
map_fig = px.scatter_geo(
    latest,
    lat="lat",
    lon="lon",
    hover_name="country",
    size="population",
    projection="natural earth",
    title="Africa Countries Overview"
)

map_pane = pn.pane.Plotly(map_fig, height=500)

# COUNTRY SELECTOR
countries = sorted(data["country"].unique())

country_select = pn.widgets.Select(
    name="Country",
    options=countries,
    value="Tunisia"
)

# DASHBOARD UPDATE FUNCTION
def update_dashboard(country):

    df = data[data["country"] == country]

    latest = df.iloc[-1]

    population = round(latest["population"] / 1_000_000, 2)
    gdp = round(latest["gdp"], 2)
    co2 = round(latest["co2"], 2)
    internet = round(latest["internet"], 2)

    indicators = pn.Row(

        pn.indicators.Number(
            name="Population",
            value=population,
            format="{value} Million",
            font_size="30pt"
        ),

        pn.indicators.Number(
            name="GDP (Billion $)",
            value=gdp,
            font_size="30pt"
        ),

        pn.indicators.Number(
            name="CO2 Emissions",
            value=co2,
            format="{value} Mt",
            font_size="30pt"
        ),

        pn.indicators.Number(
            name="Internet Users",
            value=internet,
            format="{value} %",
            font_size="30pt"
        )

    )

    fig = px.line(
        df,
        x="year",
        y="gdp",
        title=f"GDP Evolution - {country}"
    )

    chart = pn.pane.Plotly(fig, sizing_mode="stretch_width")

    return pn.Column(indicators, chart)


dashboard = pn.bind(update_dashboard, country_select)

layout = pn.Column(

    "# Africa Economic Dashboard",

    map_pane,

    "## Select a country",

    country_select,

    dashboard

)

layout.servable()
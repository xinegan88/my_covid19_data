import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from urllib.request import urlopen
import json

def generate_map(map_df):
    fig_2 = px.choropleth(map_df,
        locationmode='USA-states',
        locations='code',
        scope='usa',
        color='rate',
        labels={'rate': 'Cases per 100k residents'},
        hover_data=['state', 'cases', 'rate'],
        color_continuous_scale=px.colors.sequential.Viridis)
    fig_2.show()

def generate_bar_chart(df):
    fig = px.bar(df, x='date', y='cases_new',
        hover_data=['date', 'cases_new'], color='cases',
        labels={'cases':'Number of Cases'}, height=600)
    fig.add_trace(go.Scatter(x=df.date, y=df.cases_new_avg,
        mode='lines', name='7-day average')
        )
    fig.update_layout(
        title=go.layout.Title(text="New Cases of COVID-19"),
        yaxis_title="Number of New Cases"
        )
    fig.update_layout(
        legend=dict(
        x=0,
        y=1,
        traceorder="normal",
        font=dict(
        family="sans-serif",
        size=12,
        color="black"
        ),
        bgcolor="LightSteelBlue",
        bordercolor="Black",
        borderwidth=2
        )
        )
    fig.show()

def generate_state_bar_chart(state):
    fig = px.bar(state, x='date', y='cases_new',
        hover_data=['date', 'cases_new'], color='cases',
        labels={'cases':'number of cases'}, height=600)
    fig.add_trace(go.Scatter(x=state.date, y=state.cases_new_avg,
        mode='lines', name='7-day average')
        )
    fig.update_layout(
        title=go.layout.Title(text="New Cases of COVID-19 in " + state['state'].iloc[0]),
        yaxis_title="Number of New Cases"
        )
    fig.update_layout(
        legend=dict(
        x=0,
        y=1,
        traceorder="normal",
        font=dict(
        family="sans-serif",
        size=12,
        color="black"
        ),
        bgcolor="LightSteelBlue",
        bordercolor="Black",
        borderwidth=2
        )
        )
    fig.show()


def county_map(map_df):
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)
    fig = px.choropleth_mapbox(map_df, geojson=counties, locations='fips', color='rate',
        color_continuous_scale="Viridis",
        range_color=(0, 12),
        mapbox_style="carto-positron",
        zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
        opacity=0.5,
        labels={'rate':'infection rate'}
        )
    fig.update_layout( title_text = 'COVID-19 Infection Rate by County Per 100,000',
        geo_scope='usa', # limite map scope to USA
        )
    fig.show()

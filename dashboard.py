import copy
from re import template
from turtle import color
from matplotlib.pyplot import colorbar
from numpy import indices
import pandas as pd
import dash
import plotly
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State
from plotly.subplots import make_subplots
import statsmodels.api as sm
import datetime as dt
import plotly.io as plt_io


# eigenes Template erstellen und als default setzen
plt_io.templates["custom_dark"] = plt_io.templates["plotly_dark"]
plt_io.templates["custom_dark"]["layout"]["paper_bgcolor"] = "#272729"
plt_io.templates["custom_dark"]["layout"]["plot_bgcolor"] = "#272729"
plt_io.templates["custom_dark"]["layout"]["plot_bgcolor"] = "#272729"
plt_io.templates["custom_dark"]["layout"]["yaxis"]["gridcolor"] = "#4f687d"
plt_io.templates["custom_dark"]["layout"]["xaxis"]["gridcolor"] = "#4f687d"
plt_io.templates.default = "custom_dark"


# animierte WorldMap erstellen
# source for categories https://mahshadn.medium.com/animated-choropleth-map-with-discrete-colors-using-python-and-plotly-styling-5e208e5b6bf8
wars = pd.read_csv("datasets//war_and_peace.csv")

# Kategorien erstellen für unique Legendeneinträge
wars["category"] = ""


def set_cat(row):
    if row["type_of_conflict"] == 1:
        return "außersystemisch"
    if row["type_of_conflict"] == 2:
        return "zwischenstaatlich"
    if row["type_of_conflict"] == 3:
        return "innerstaatlich"
    if row["type_of_conflict"] == 4:
        return "international innerstaatlich"


wars = wars.assign(category=wars.apply(set_cat, axis=1))
wars = wars.sort_values("year", ascending=True)
catg = wars["category"].unique()
dts = wars["year"].unique()

for tf in dts:
    for i in catg:
        wars = pd.concat(
            [
                wars,
                pd.DataFrame.from_records(
                    [{"year": tf, "type_of_conflict": "N", "category": i}]
                ),
            ]
        )


worldmap = px.choropleth(
    wars,
    locations="location",
    color="category",
    animation_frame="year",
    animation_group="type_of_conflict",
    locationmode="country names",
    hover_data=[
        "side_b",
        "territory_name",
        "intensity_level",
    ],
    color_discrete_map={"1": "#82CCF8", "2": "#68D1DE", "3": "#68DEA9", "4": "#75F999"},
    category_orders={
        "category": [
            "außersystemisch",
            "zwischenstaatlich",
            "innerstaatlich",
            "international innerstaatlich",
        ]
    },
    scope="world",
    height=573,
    title="Weltweite Konflikte nach Jahr und Art",
    range_color=(1, 4),
    labels={
        "year": "Jahr",
        "location": "Land",
        "category": "<b>Konfliktart</b>",
        "side_b": "Gegenseite",
        "territory_name": "Region",
        "intensity_level": "Intensität",
    },
)

worldmap.update_layout(
    showlegend=True,
    margin={"r": 0, "t": 40, "l": 0, "b": 0},
    legend=dict(orientation="v"),
)


# Dataframes


# Testdata einlesen (für die Tabelle mit Annotations)
testdata = pd.read_csv("datasets//testdata.csv")
testdata["year"] = pd.to_datetime(testdata["year"], format="%Y")
# Array
testkip = []
for kip in testdata:
    testkip.append({"label": str(kip), "value": kip})
# Figure
# TODO: Annotationsplatzhalter Figure
figgy = px.line(testdata, x="year", y="Gesamtbevölkerung")
figgy.update_layout(title_text="Gesamtbevölkerung")


# ÖlPreise für erstes DIV
oil_prices = pd.read_csv("datasets//oil_brent_texas.csv", header=[0])


# KIP Ländertabelle
# kpi_table = pd.read_csv('datasets//kpi_table.csv')
kpi_table = pd.read_csv("datasets//g8_kpi_table.csv")
kpi_table = kpi_table.astype({"year": int})


# Einlesen der Konflikttabelle HIIK
war_table = pd.read_csv("datasets//war_table.csv")
war_table = war_table.astype({"year": int})


# Einlesen der Konflikttabelle ourworldindata
war_table_owid = pd.read_csv("datasets//war_table_two.csv", sep=";")
war_table_owid = war_table_owid.astype({"year": int})


# Einlesen der Google Trends für Konflikte
google_trends_conflicts = pd.read_csv("datasets//conflicts_google_trends.csv")


# TODO: Einlesen der Verhältnisse zwischen Suchanfragen
google_trends_afg_ukr_absolute = pd.read_csv("datasets//afg_ukr_difference.csv")


# Einlesen der YouTube Trends für Konflikte
youtube_trends_conflicts = pd.read_csv("datasets//yt_trends.csv")


# Rename der Tabellenköpfe


# Rename der Google-Trends Tabellenköpfe
google_trends_conflicts = google_trends_conflicts.rename(
    columns={
        "afg_2010_germany": "Karfreitagsgefecht Afghanistan 2010 (DEU)",
        "afg_2010_world": "Karfreitagsgefecht Afghanistan 2010 (WLD)",
        "afg_2021_germany": "Machtübernahme Taliban in Afghanistan 2021 (DEU)",
        "afg_2021_world": "Machtübernahme Taliban in Afghanistan 2021 (WLD)",
        "irak_2020_germany": "Irakkrise Anfang 2020 (DEU)",
        "irak_2020_world": "Irakkrise Anfang 2020 (WLD)",
        "ukr_2014_germany": "Annexion der Krim durch Russland 2014 (DEU)",
        "ukr_2014_world": "Annexion der Krim durch Russland 2014 (WLD)",
        "ukr_2022_germany": "Angriff Russland auf die Ukraine 2022 (DEU)",
        "ukr_2022_world": "Angriff Russland auf die Ukraine 2022 (WLD)",
    }
)


# Rename der YouTube-Trends Tabellenköpfe
youtube_trends_conflicts = youtube_trends_conflicts.rename(
    columns={
        "afg_2010_ger": "Karfreitagsgefecht Afghanistan 2010 (DEU)",
        "afg_2010_wld": "Karfreitagsgefecht Afghanistan 2010 (WLD)",
        "afg_2021_ger": "Machtübernahme Taliban in Afghanistan 2021 (DEU)",
        "afg_2021_wld": "Machtübernahme Taliban in Afghanistan 2021 (WLD)",
        "irak_2020_ger": "Irakkrise Anfang 2020 (DEU)",
        "irak_2020_wld": "Irakkrise Anfang 2020 (WLD)",
        "ukr_2014_ger": "Annexion der Krim durch Russland 2014 (DEU)",
        "ukr_2014_wld": "Annexion der Krim durch Russland 2014 (WLD)",
        "ukr_2022_ger": "Angriff Russland auf die Ukraine 2022 (DEU)",
        "ukr_2022_wld": "Angriff Russland auf die Ukraine 2022 (WLD)",
    }
)


# Rename der KIP Tabellenköpfe
kpi_table = kpi_table.rename(
    columns={
        "gdp_growth": "BIP Wachstum zum Vorjahr in %",
        "gdp_usd": "BIP in USD",
        "military_spendings_growth": "Militärausgaben in % zum BIP",
        "military_spendings_usd": "Militärausgaben in USD",
        "gni_usd": "BNI in USD",
        "gni_growth": "BNI in Wachstum zum Vorjahr in %",
        "energy_use": "Energienutzung in Kg",
        "national_income_usd": "Nettnationaleinkommen in USD",
        "national_income_growth": "Nettonationaleinkommen Wachstum zum Vorjahr",
    }
)


# Rename der Konflikttabellenköpfe
war_table = war_table.rename(
    columns={
        "dispute": "Dispute",
        "non_violent_crises": "gewaltlose Kriege",
        "violent_crises": "gewaltsame Kriege",
        "limited_wars": "begrenzte Kriege",
        "wars": "Kriege",
        "total": "Gesamt",
    }
)


# Rename der KIP Tabellenköpfe
oil_prices = oil_prices.rename(
    columns={
        "price_texas": "WTI (USD je Barrel)",
        "price_brent": "UK Brent (USD je Barrel)",
    }
)


# Arrays für Dropdownmenüs


# KIP Array für Dropdown
kip_options = []
for kip in kpi_table:
    kip_options.append({"label": str(kip), "value": kip})


# Country Array für Dropdown
country_options = []
for country in kpi_table["country_name"].unique():
    country_options.append({"label": str(country), "value": country})


# HIIK Conflict Array für Dropdown
conflict_options = []
for conflict in war_table:
    conflict_options.append({"label": str(conflict), "value": conflict})

# ourworldindata Conflict Array für Dropdown
conflict_options_owid = []
for conflict in war_table_owid:
    conflict_options_owid.append({"label": str(conflict), "value": conflict})


# Figures


# YouTube-TrendsConflicts
fig_yt_trends_conflicts = px.scatter(
    youtube_trends_conflicts,
    x="week",
    y=youtube_trends_conflicts.columns,
    title="<b>Google-Trends</b> in Wochen",
    trendline="lowess",
    template="custom_dark",
    trendline_scope="overall",
    labels={
        "week": "Woche",
        "value": "<b>Suchanfragen</b> in %",
        "variable": "<b>Konflikt</b><br>",
    },
)
fig_yt_trends_conflicts.update_traces(mode="lines+markers")

# Google-TrendsConflicts
fig_google_trends_conflicts = px.scatter(
    google_trends_conflicts,
    x="week",
    y=google_trends_conflicts.columns,
    title="<b>Google-Trends</b> in Wochen",
    trendline="lowess",
    trendline_scope="overall",
    labels={
        "week": "Woche",
        "value": "<b>Suchanfragen</b> in %",
        "variable": "<b>Konflikt</b><br>",
    },
)
fig_google_trends_conflicts.update_traces(mode="lines+markers")


# Dashapp
app = Dash(__name__)

# AppLayout
app.layout = html.Div(
    children=[
        # Titeldiv
        html.Div(
            children=[
                html.H3(children="global conflicts data"),
                html.H6(
                    children="Bachelor Thesis 2022",
                    style={"marginTop": "-20px", "marginBottom": "30px"},
                ),
            ],
            style={"textAlign": "center"},
        ),
        # Box Reihe
        # html.Div(children=[
        #     # Boxes Div für spätere KIPs
        #     html.Div(children=[
        #         html.Div(children=[
        #             html.H3('Test', style={'fontWeight': 'bold'}),
        #             html.Label('Datensätze', style={'paddingTop': '.3rem'}), ], className="two columns",
        #             style={'padding': '2rem', 'marginLeft': '1rem',  'border-radius': '0px', 'marginTop': '2rem', 'background-color': '#272729'}),
        #         html.Div(children=[
        #             html.H3('Test', style={'fontWeight': 'bold'}),
        #             html.Label('Datensätze', style={'paddingTop': '.3rem'}), ], className="two columns",
        #             style={'padding': '2rem', 'marginLeft': '2rem',  'border-radius': '0px', 'marginTop': '2rem', 'backgroundColor': '#272729', }),
        #         html.Div(children=[
        #             html.H3('Test', style={'fontWeight': 'bold'}),
        #             html.Label('Datensätze', style={'paddingTop': '.3rem'}), ], className="two columns",
        #             style={'padding': '2rem', 'marginLeft': '2rem',  'border-radius': '0px', 'marginTop': '2rem', 'backgroundColor': '#272729', }),
        #         html.Div(children=[
        #             html.H3('Test', style={'fontWeight': 'bold'}),
        #             html.Label('Datensätze', style={'paddingTop': '.3rem'}), ], className="two columns",
        #             style={'padding': '2rem', 'marginLeft': '2rem',  'border-radius': '0px', 'marginTop': '2rem', 'backgroundColor': '#272729', }),
        #         html.Div(children=[
        #             html.H3('Test', style={'fontWeight': 'bold'}),
        #             html.Label('Datensätze', style={'paddingTop': '.3rem'}), ], className="two columns",
        #             style={'padding': '2rem', 'marginLeft': '2rem',  'border-radius': '0px', 'marginTop': '2rem', 'backgroundColor': '#272729', }),
        #         html.Div(children=[
        #             html.H3('Test', style={'fontWeight': 'bold'}),
        #             html.Label('Datensätze', style={'paddingTop': '.3rem'}), ], className="two columns",
        #             style={'padding': '2rem', 'marginLeft': '2rem',  'border-radius': '0px', 'marginTop': '2rem', 'backgroundColor': '#272729', }),
        #     ], className="twelve columns")
        # ]),
        # Div erste Reihe
        html.Div(
            className="twelve columns",
            children=[
                # Div Erklärung erste Reihe
                html.Div(
                    children=[
                        html.H4(children="Konflikte und die Weltwirtschaft"),
                        html.H6(
                            children="Erklärung",
                            style={"marginTop": "-15px", "marginBottom": "30px"},
                        ),
                        html.P(
                            children="Der linke Graph zeigt eine animierte Weltkarte mit allen Konflikten weltweit von 1946 bis 2020."
                        ),
                        html.P(
                            children="Der rechte Graph zeigt weltwirtschaftliche Kennzahlen, welche über das Dropdownmenü ausgewählt werden können. Über das Eingabe- und Datumsfeld, können Anemrkungen auf dem Graphen hinzugefügt werden."
                        ),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Label(
                            children="Datenquellen: ", style={"font-weight": "bold"}
                        ),
                        html.A(
                            children="The World Bank Data",
                            href="https://databank.worldbank.org/source/world-development-indicators",
                            target="_blank",
                        ),
                    ],
                    className="two columns",
                    style={
                        "padding": "2rem",
                        "margin": "1rem",
                        "border-radius": "0px",
                        "marginTop": "2rem",
                        "background-color": "#272729",
                    },
                ),
                # Div Worldmap
                html.Div(
                    className="five columns",
                    style={
                        "padding": "2rem",
                        "margin": "1rem",
                        "border-radius": "0px",
                        "marginTop": "2rem",
                        "backgroundColor": "#272729",
                    },
                    children=[dcc.Graph(id="worldmap_graph", figure=worldmap)],
                ),
                # Div World KIPs mit Annotationen
                html.Div(
                    children=[
                        dcc.Dropdown(
                            id="world_kip_picker",
                            options=testkip[1:],
                            style={"width": "77.5%", "marginBottom": ".5rem"},
                            clearable=False,
                            searchable=True,
                            placeholder="KPI auswählen..",
                        ),
                        html.Div(
                            children=[
                                dcc.Input(
                                    id="textarea",
                                    style={"width": "60%"},
                                    placeholder="Ihre Eingabe...",
                                    type="text",
                                )
                            ]
                        ),
                        dcc.DatePickerSingle(
                            id="date-picker-single",
                            style={"marginTop": ".5rem"},
                            date="2017-06-21",
                            display_format="DD.MM.YYYY",
                        ),
                        html.Button(
                            "submit", id="submit", style={"marginLeft": ".3rem"}
                        ),
                        html.Button("clear", id="clear", style={"marginLeft": ".3rem"}),
                        dcc.Graph(id="testgraph", figure=figgy),
                    ],
                    className="five columns",
                    style={
                        "padding": "2rem",
                        "margin": "1rem",
                        "border-radius": "0px",
                        "marginTop": "2rem",
                        "backgroundColor": "#272729",
                    },
                ),
            ],
        ),
        # Div zweite Reihe
        html.Div(
            className="twelve columns",
            children=[
                # Div Erklärung zweite Reihe
                html.Div(
                    children=[
                        html.H4(
                            children="Konfliktart vs Wirtschaft in den G8+5 Staaten"
                        ),
                        html.H6(
                            children="Erklärung",
                            style={"marginTop": "-15px", "marginBottom": "30px"},
                        ),
                        html.P(
                            children="Diese Graphen zeigen das Verhältnis der KPIs der G8+5 Staaten in Verhältnis zu den Konflikten nach HIIK und Our World in Data."
                        ),
                        html.P(
                            children="Links werden die KPIs mit den Konflikten nach dem HIIK gezeigt. Rechts werden die KPIs mit den Konflikten nach Our World in Data visualisiert."
                        ),
                        html.Br(),
                        html.Br(),
                        html.Label(
                            children="Datenquellen: ", style={"font-weight": "bold"}
                        ),
                        html.A(
                            children="Konfliktarten nach HIIK",
                            href="https://de.statista.com/statistik/daten/studie/2736/umfrage/entwicklung-der-anzahl-von-konflikten-weltweit/",
                            target="_blank",
                        ),
                        html.Br(),
                        html.A(
                            children="Konfliktarten nach PRIO/UCDP/OWID",
                            href="https://de.statista.com/statistik/daten/studie/168188/umfrage/anzahl-internationale-konflikte/",
                            target="_blank",
                        ),
                        html.Br(),
                        html.A(
                            children="The World Bank Data",
                            href="https://databank.worldbank.org/source/world-development-indicators",
                            target="_blank",
                        ),
                    ],
                    className="two columns",
                    style={
                        "padding": "2rem",
                        "margin": "1rem",
                        "border-radius": "0px",
                        "marginTop": "2rem",
                        "background-color": "#272729",
                    },
                ),
                # Div Linechart Länder, KIPS, HIIK Konflikte
                html.Div(
                    children=[
                        dcc.Dropdown(
                            id="country_picker",
                            options=country_options,
                            optionHeight=35,  # height/space between dropdown options
                            value="Germany",  # dropdown value selected automatically when page loads
                            disabled=False,  # disable dropdown value selection
                            multi=False,  # allow multiple dropdown values to be selected
                            searchable=True,  # allow user-searching of dropdown values
                            search_value="",  # remembers the value searched in dropdown
                            # gray, default text shown when no option is selected
                            placeholder="Please select...",
                            clearable=False,  # allow user to removes the selected value
                            # use dictionary to define CSS styles of your dropdown
                            style={"width": "77.5%", "marginBottom": ".5rem"},
                            # className='select_box',           #activate separate CSS document in assets folder
                            # persistence=True,                 #remembers dropdown value. Used with persistence_type
                            # persistence_type='memory'         #remembers dropdown value selected until...
                        ),
                        dcc.Dropdown(
                            id="kip_picker",
                            options=kip_options[2:],
                            optionHeight=35,  # height/space between dropdown options
                            # dropdown value selected automatically when page loads
                            value="BIP Wachstum zum Vorjahr in %",
                            disabled=False,  # disable dropdown value selection
                            multi=False,  # allow multiple dropdown values to be selected
                            searchable=True,  # allow user-searching of dropdown values
                            search_value="",  # remembers the value searched in dropdown
                            # gray, default text shown when no option is selected
                            placeholder="Please select...",
                            clearable=False,  # allow user to removes the selected value
                            # use dictionary to define CSS styles of your dropdown
                            style={"width": "77.5%", "marginBottom": ".5rem"},
                            # className='select_box',           #activate separate CSS document in assets folder
                            # persistence=True,                 #remembers dropdown value. Used with persistence_type
                            # persistence_type='memory'         #remembers dropdown value selected until...
                        ),
                        dcc.Dropdown(
                            id="conflict_picker",
                            options=conflict_options[1:],
                            optionHeight=35,  # height/space between dropdown options
                            # dropdown value selected automatically when page loads
                            value="Gesamt",
                            disabled=False,  # disable dropdown value selection
                            multi=False,  # allow multiple dropdown values to be selected
                            searchable=True,  # allow user-searching of dropdown values
                            search_value="",  # remembers the value searched in dropdown
                            # gray, default text shown when no option is selected
                            placeholder="Please select...",
                            clearable=False,  # allow user to removes the selected value
                            # use dictionary to define CSS styles of your dropdown
                            style={"width": "77.5%", "marginBottom": ".5rem"},
                            # className='select_box',           #activate separate CSS document in assets folder
                            # persistence=True,                 #remembers dropdown value. Used with persistence_type
                            # persistence_type='memory'         #remembers dropdown value selected until...
                        ),
                        dcc.Graph(id="country_kip_graph"),
                    ],
                    className="five columns",
                    style={
                        "padding": "2rem",
                        "margin": "1rem",
                        "border-radius": "0px",
                        "marginTop": "2rem",
                        "backgroundColor": "#272729",
                    },
                ),
                # DIV World KIPS, HIIK Konflikte
                html.Div(
                    children=[
                        dcc.Dropdown(
                            id="country_picker_two",
                            options=country_options,
                            optionHeight=35,  # height/space between dropdown options
                            value="Germany",  # dropdown value selected automatically when page loads
                            disabled=False,  # disable dropdown value selection
                            multi=False,  # allow multiple dropdown values to be selected
                            searchable=True,  # allow user-searching of dropdown values
                            search_value="",  # remembers the value searched in dropdown
                            # gray, default text shown when no option is selected
                            placeholder="Please select...",
                            clearable=False,  # allow user to removes the selected value
                            # use dictionary to define CSS styles of your dropdown
                            style={"width": "77.5%", "marginBottom": ".5rem"},
                            # className='select_box',           #activate separate CSS document in assets folder
                            # persistence=True,                 #remembers dropdown value. Used with persistence_type
                            # persistence_type='memory'         #remembers dropdown value selected until...
                        ),
                        dcc.Dropdown(
                            id="kip_picker_two",
                            options=kip_options[2:],
                            optionHeight=35,  # height/space between dropdown options
                            # dropdown value selected automatically when page loads
                            value="BIP Wachstum zum Vorjahr in %",
                            disabled=False,  # disable dropdown value selection
                            multi=False,  # allow multiple dropdown values to be selected
                            searchable=True,  # allow user-searching of dropdown values
                            search_value="",  # remembers the value searched in dropdown
                            # gray, default text shown when no option is selected
                            placeholder="Please select...",
                            clearable=False,  # allow user to removes the selected value
                            # use dictionary to define CSS styles of your dropdown
                            style={"width": "77.5%", "marginBottom": ".5rem"},
                            # className='select_box',           #activate separate CSS document in assets folder
                            # persistence=True,                 #remembers dropdown value. Used with persistence_type
                            # persistence_type='memory'         #remembers dropdown value selected until...
                        ),
                        dcc.Dropdown(
                            id="conflict_picker_two",
                            options=conflict_options_owid[1:],
                            optionHeight=35,  # height/space between dropdown options
                            # dropdown value selected automatically when page loads
                            value="Gesamt",
                            disabled=False,  # disable dropdown value selection
                            multi=False,  # allow multiple dropdown values to be selected
                            searchable=True,  # allow user-searching of dropdown values
                            search_value="",  # remembers the value searched in dropdown
                            # gray, default text shown when no option is selected
                            placeholder="Please select...",
                            clearable=False,  # allow user to removes the selected value
                            # use dictionary to define CSS styles of your dropdown
                            style={"width": "77.5%", "marginBottom": ".5rem"},
                            # className='select_box',           #activate separate CSS document in assets folder
                            # persistence=True,                 #remembers dropdown value. Used with persistence_type
                            # persistence_type='memory'         #remembers dropdown value selected until...
                        ),
                        dcc.Graph(id="country_kip_graph_owid"),
                    ],
                    className="five columns",
                    style={
                        "padding": "2rem",
                        "margin": "1rem",
                        "border-radius": "0px",
                        "marginTop": "2rem",
                        "backgroundColor": "#272729",
                    },
                ),
            ],
        ),
        # Div dritte Reihe
        html.Div(
            className="twelve columns",
            children=[
                # Div dritte Reihe Erklärung
                html.Div(
                    children=[
                        html.H4(children="Google-Trends: Konflikte"),
                        html.H6(
                            children="Erklärung",
                            style={"marginTop": "-15px", "marginBottom": "30px"},
                        ),
                        html.P(
                            children="Diese Graphen zeigen die Anzahl der Google-Suchanfragen in einer jeweiligen Woche in Prozent zum höchsten Wert. 100 bedeutet, dass in dieser Woche die meisten Suchanfragen zu dieser Konfliktregion abgeschickt wurden."
                        ),
                        html.P(children="Der Graph auf der rechten Seite ist noch"),
                        html.P(children="(DEU) steht für Suchanfragen aus Deutschland"),
                        html.P(children="(WLD) steht für weltweite Suchanfragen"),
                        html.P(
                            children="Mit einem Klick auf den Button wechselt man zwischen Google- und YouTube-Suchanfragen."
                        ),
                        html.Br(),
                        html.Br(),
                        html.Label(
                            children="Datenquellen: ", style={"font-weight": "bold"}
                        ),
                        html.A(
                            children="Google-Trends",
                            href="https://www.google.com/trends",
                            target="_blank",
                        ),
                    ],
                    className="two columns",
                    style={
                        "padding": "2rem",
                        "margin": "1rem",
                        "border-radius": "0px",
                        "marginTop": "2rem",
                        "background-color": "#272729",
                    },
                ),
                # Div YouTube/Google Trends 100
                html.Div(
                    children=[
                        html.Button(
                            "Toggle YouTube/Google",
                            id="toggle_yt_google_trends",
                            n_clicks=0,
                        ),
                        dcc.Graph(
                            id="google_trends_conflicts_graph",
                            figure=fig_google_trends_conflicts,
                        ),
                    ],
                    className="five columns",
                    style={
                        "padding": "2rem",
                        "margin": "1rem",
                        "border-radius": "0px",
                        "marginTop": "2rem",
                        "backgroundColor": "#272729",
                    },
                ),
                # Div YouTube/Google Trends non 100
                html.Div(
                    children=[
                        html.Button(
                            "Trendlinie on/off", id="trendline_on_off", n_clicks=0
                        ),
                        dcc.Graph(id="google_trends_afg_ukr"),
                    ],
                    className="five columns",
                    style={
                        "padding": "2rem",
                        "margin": "1rem",
                        "border-radius": "0px",
                        "marginTop": "2rem",
                        "backgroundColor": "#272729",
                    },
                ),
            ],
        ),
    ]
)


# Callbacks
# Annotationcallback zweites Div erste Reihe
@app.callback(
    Output(component_id="testgraph", component_property="figure"),
    Input(component_id="submit", component_property="n_clicks"),
    Input(component_id="clear", component_property="n_clicks"),
    State(component_id="date-picker-single", component_property="date"),
    State(component_id="textarea", component_property="value"),
    State(component_id="testgraph", component_property="figure"),
    Input(component_id="world_kip_picker", component_property="value"),
)
def update_output_div(n_clicks, value, dates, conflict, fig, kip):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    figure = plotly.graph_objects.Figure(fig)

    if trigger_id == "world_kip_picker":
        figure = px.line(testdata, x="year", y=str(kip))
        figure.update_layout(title_text=str(kip))
    else:
        if trigger_id == "submit":
            figure.add_vline(
                x=dt.datetime.strptime(dates, "%Y-%m-%d").timestamp() * 1000,
                annotation_text=conflict,
                line_width=3,
                line_dash="dash",
                line_color="green",
            )
        else:
            figure = figgy

    return figure


# Callback G8+5 Chart erstes Div zweite Reihe
@app.callback(
    Output(component_id="country_kip_graph", component_property="figure"),
    Input(component_id="country_picker", component_property="value"),
    Input(component_id="kip_picker", component_property="value"),
    Input(component_id="conflict_picker", component_property="value"),
)
def build_graph(country_chosen, kip_chosen, conflict_chosen):
    copy = kpi_table
    dff = copy[copy["country_name"] == country_chosen]
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(
            x=war_table["year"],
            y=war_table[conflict_chosen],
            name=str(conflict_chosen),
            marker_color="#82CCF8",
            mode="lines+markers",
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=dff["year"], y=dff[kip_chosen], name=str(kip_chosen), mode="lines+markers"
        ),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text="Verhältnis Konfliktart vs <b>"
        + str(kip_chosen)
        + "</b> in <b>"
        + str(country_chosen)
        + "</b>"
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Jahr", range=[2001, 2022])
    # fig.data[1].update(xaxis='x2')

    # Set y-axes titles
    fig.update_yaxes(title_text=f"Anzahl {str(conflict_chosen)}", secondary_y=False)
    fig.update_yaxes(title_text=str(kip_chosen), secondary_y=True)

    return fig


# Callback Oilprices Chart zweites Div zweite Reihe
@app.callback(
    Output(component_id="country_kip_graph_owid", component_property="figure"),
    Input(component_id="country_picker_two", component_property="value"),
    Input(component_id="kip_picker_two", component_property="value"),
    Input(component_id="conflict_picker_two", component_property="value"),
)
def build_graph(country_chosen, kip_chosen, conflict_chosen):
    copy = kpi_table
    dff = copy[copy["country_name"] == country_chosen]
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(
            x=war_table_owid["year"],
            y=war_table_owid[conflict_chosen],
            name=str(conflict_chosen),
            marker_color="#82CCF8",
            mode="lines+markers",
            #    opacity=0.5
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=dff["year"], y=dff[kip_chosen], name=str(kip_chosen), mode="lines+markers"
        ),
        secondary_y=True,
    )

    # secon xaxis
    fig.update_layout(xaxis2={"anchor": "y", "overlaying": "x", "side": "top"})

    # Add figure title
    fig.update_layout(
        title_text="Verhältnis Konfliktart vs <b>"
        + str(kip_chosen)
        + "</b> in <b>"
        + str(country_chosen)
        + "</b>"
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Jahr", range=[2001, 2022])
    # fig.data[1].update(xaxis='x2')

    # Set y-axes titles
    fig.update_yaxes(title_text=f"Anzahl {str(conflict_chosen)}", secondary_y=False)
    fig.update_yaxes(title_text=str(kip_chosen), secondary_y=True)

    return fig


# Callback YT Google toggle erstes Div dritte Reihe
@app.callback(
    Output(component_id="google_trends_conflicts_graph", component_property="figure"),
    [Input("toggle_yt_google_trends", "n_clicks")],
)
def update_output_div(n_clicks):

    if (n_clicks % 2) == 0:
        fig = fig_google_trends_conflicts
        fig.update_layout(title="<b>Google-Trends</b> in Wochen")
    else:
        fig = fig_yt_trends_conflicts
        fig.update_layout(title="<b>YouTube-Trends</b> in Wochen")
    return fig


# Trendline Callback zweites Div dritte Reihe
@app.callback(
    Output(component_id="google_trends_afg_ukr", component_property="figure"),
    [Input("trendline_on_off", "n_clicks")],
)
def update_output_div(n_clicks):
    df = google_trends_afg_ukr_absolute

    if (n_clicks % 2) == 0:
        fig = px.scatter(
            df,
            x="week",
            y=df.columns,
            trendline="lowess",
            title="<b>Google-Trends</b> in Wochen",
            labels={
                "week": "Woche",
                "value": "<b>Suchanfragen</b> in %",
                "variable": "<b>Konflikt</b><br>",
            },
        )
        fig.update_traces(mode="lines+markers")

    else:
        fig = px.scatter(
            df,
            x="week",
            y=df.columns,
            title="<b>Google-Trends</b> in Wochen",
            labels={
                "week": "Woche",
                "value": "<b>Suchanfragen</b> in %",
                "variable": "<b>Konflikt</b><br>",
            },
        )
        fig.update_traces(mode="lines+markers")

    return fig


# Appstart
if __name__ == "__main__":
    app.run_server(debug=True)

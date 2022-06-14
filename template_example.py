import copy
from re import template
from turtle import color
from numpy import indices
import pandas as pd
import dash
import plotly
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State
from plotly.subplots import make_subplots
import statsmodels.api as sm
import datetime as dt


df_count = 0

# Dataframes

# Testdata einlesen
testdata = pd.read_csv('testdata.csv')
testdata['year'] = pd.to_datetime(
    testdata['year'], format='%Y')
# Array
testkip = []
for kip in testdata:
    testkip.append({'label': str(kip), 'value': kip})


# ÖlPreise für erstes DIV
oil_prices = pd.read_csv('datasets\\oil_brent_texas.csv', header=[0])

# TODO: Annotationsdiv  Gesamttabelle erstellen
oil_prices_annotations = pd.read_csv(
    'datasets\\oil_brent_texas.csv', header=[0])
oil_prices_annotations['year'] = pd.to_datetime(
    oil_prices_annotations['year'], format='%Y')

df_count += 1

# KIP Ländertabelle
bachelor_table = pd.read_csv('datasets\\bachelor_table.csv')
bachelor_table = bachelor_table.astype({'year': int})
df_count += 1

# Einlesen der Konflikttabelle
war_table = pd.read_csv('datasets\war_table.csv')
war_table = war_table.astype({'year': int})
df_count += 1

# Einlesen der Google Trends für Konflikte
google_trends_conflicts = pd.read_csv('datasets\\conflicts_google_trends.csv')
df_count += 1

# TODO: Einlesen der Verhältnisse zwischen Suchanfragen
google_trends_afg_ukr_absolute = pd.read_csv(
    'datasets\\afg_ukr_difference.csv')
df_count += 1

# Einlesen der YouTube Trends für Konflikte
youtube_trends_conflicts = pd.read_csv('datasets\\yt_trends.csv')

# Rename der Google-Trends Tabellenköpfe
google_trends_conflicts = google_trends_conflicts.rename(columns={
    'afg_2010_germany': 'Karfreitagsgefecht Afghanistan 2010 (DEU)',
    'afg_2010_world': 'Karfreitagsgefecht Afghanistan 2010 (WLD)',
    'afg_2021_germany': 'Machtübernahme Taliban in Afghanistan 2021 (DEU)',
    'afg_2021_world': 'Machtübernahme Taliban in Afghanistan 2021 (WLD)',
    'irak_2020_germany': 'Irakkrise Anfang 2020 (DEU)',
    'irak_2020_world': 'Irakkrise Anfang 2020 (WLD)',
    'ukr_2014_germany': 'Annexion der Krim durch Russland 2014 (DEU)',
    'ukr_2014_world': 'Annexion der Krim durch Russland 2014 (WLD)',
    'ukr_2022_germany': 'Angriff Russland auf die Ukraine 2022 (DEU)',
    'ukr_2022_world': 'Angriff Russland auf die Ukraine 2022 (WLD)',
})

# Rename der YouTube-Trends Tabellenköpfe
youtube_trends_conflicts = youtube_trends_conflicts.rename(columns={
    'afg_2010_ger': 'Karfreitagsgefecht Afghanistan 2010 (DEU)',
    'afg_2010_wld': 'Karfreitagsgefecht Afghanistan 2010 (WLD)',
    'afg_2021_ger': 'Machtübernahme Taliban in Afghanistan 2021 (DEU)',
    'afg_2021_wld': 'Machtübernahme Taliban in Afghanistan 2021 (WLD)',
    'irak_2020_ger': 'Irakkrise Anfang 2020 (DEU)',
    'irak_2020_wld': 'Irakkrise Anfang 2020 (WLD)',
    'ukr_2014_ger': 'Annexion der Krim durch Russland 2014 (DEU)',
    'ukr_2014_wld': 'Annexion der Krim durch Russland 2014 (WLD)',
    'ukr_2022_ger': 'Angriff Russland auf die Ukraine 2022 (DEU)',
    'ukr_2022_wld': 'Angriff Russland auf die Ukraine 2022 (WLD)',
})

# Rename der Tabellenköpfe

# Rename der KIP Tabellenköpfe
bachelor_table = bachelor_table.rename(columns={
    'brithrate': 'Geburtenrate per 1000 Einwohner',
    'gdp_growth': 'BIP Wachstum zum Vorjahr in %',
    'gdp_usd': 'BIP in USD',
    'military_spendings_growth': 'Militärausgaben zum Vorjahr in %',
    'military_spendings_usd': 'Militärausgaben in USD',
    'life_exp': 'Lebenserwartung in Jahren',
    'energy_use': 'Energienutzung in Kg',
})

# Rename der Konflikttabellenköpfe
war_table = war_table.rename(columns={
    'dispute': 'Dispute',
    'non_violent_crises': 'gewaltlose Kriege',
    'violent_crises': 'gewaltsame Kriege',
    'limited_wars': 'begrenzte Kriege',
    'wars': 'Kriege',
    'total': 'Gesamt',
})

# Rename der KIP Tabellenköpfe
oil_prices = oil_prices.rename(columns={
    'price_texas': 'WTI (USD je Barrel)',
    'price_brent': 'UK Brent (USD je Barrel)',
})

# TODO:Rename der Ölpreisannotationentabelle. Anpassen wenn mehr KIPs da sind
oil_prices_annotations = oil_prices_annotations.rename(columns={
    'price_texas': 'WTI (USD je Barrel)',
    'price_brent': 'UK Brent (USD je Barrel)',
})

# Arrays für Dropdownmenüs

# KIP Array für Dropdown
kip_options = []
for kip in bachelor_table:
    kip_options.append({'label': str(kip), 'value': kip})

# Country Array für Dropdown
country_options = []
for country in bachelor_table['country_name'].unique():
    country_options.append({'label': str(country), 'value': country})

# Conflict Array für Dropdown
conflict_options = []
for conflict in war_table:
    conflict_options.append({'label': str(conflict), 'value': conflict})

# Figures
# TODO: Annotationsplatzhalter Figure
figgy = px.line(testdata, x='year',
                y='Gesamtbevölkerung')

# YouTube-TrendsConflicts
fig_yt_trends_conflicts = px.scatter(
    youtube_trends_conflicts, x='week', y=youtube_trends_conflicts.columns, title="<b>Google-Trends</b> in Wochen", labels={
        'week': 'Woche',
        'value': '<b>Suchanfragen</b> in %',
        'variable': '<b>Konflikt</b><br>'
    })
fig_yt_trends_conflicts.update_traces(mode='lines+markers')

# Google-TrendsConflicts
fig_google_trends_conflicts = px.scatter(
    google_trends_conflicts, x='week', y=google_trends_conflicts.columns, title="<b>Google-Trends</b> in Wochen", labels={
        'week': 'Woche',
        'value': '<b>Suchanfragen</b> in %',
        'variable': '<b>Konflikt</b><br>'
    })
fig_google_trends_conflicts.update_traces(mode='lines+markers')


# Dashapp
app = Dash(__name__)

# AppLayout
app.layout = html.Div(children=[

    #
    html.Div(children=[
        html.H3(children='global conflicts data'),
        html.H6(children='Bachelor Thesis 2022',
                style={'marginTop': '-20px', 'marginBottom': '30px'})
    ], style={'textAlign': 'center'}),

    html.Div(children=[
        ################### Filter box ######################



        ##### HERE insert the code for four boxes & graph #########
        html.Div(children=[
            html.Div(children=[
                html.H3(df_count, style={'fontWeight': 'bold'}),
                html.Label('Datensätze', style={'paddingTop': '.3rem'}), ], className="two columns",
                style={'padding': '2rem', 'marginLeft': '1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'marginTop': '2rem', 'background-color': 'white'}),
            html.Div(children=[
                html.H3(df_count, style={'fontWeight': 'bold'}),
                html.Label('Datensätze', style={'paddingTop': '.3rem'}), ], className="two columns",
                style={'padding': '2rem', 'marginLeft': '2rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'marginTop': '2rem', 'backgroundColor': 'white', }),
            html.Div(children=[
                html.H3(df_count, style={'fontWeight': 'bold'}),
                html.Label('Datensätze', style={'paddingTop': '.3rem'}), ], className="two columns",
                style={'padding': '2rem', 'marginLeft': '2rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'marginTop': '2rem', 'backgroundColor': 'white', }),
            html.Div(children=[
                html.H3(df_count, style={'fontWeight': 'bold'}),
                html.Label('Datensätze', style={'paddingTop': '.3rem'}), ], className="two columns",
                style={'padding': '2rem', 'marginLeft': '2rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'marginTop': '2rem', 'backgroundColor': 'white', }),
            html.Div(children=[
                html.H3(df_count, style={'fontWeight': 'bold'}),
                html.Label('Datensätze', style={'paddingTop': '.3rem'}), ], className="two columns",
                style={'padding': '2rem', 'marginLeft': '2rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'marginTop': '2rem', 'backgroundColor': 'white', }),
            html.Div(children=[
                html.H3(df_count, style={'fontWeight': 'bold'}),
                html.Label('Datensätze', style={'paddingTop': '.3rem'}), ], className="two columns",
                style={'padding': '2rem', 'marginLeft': '2rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'marginTop': '2rem', 'backgroundColor': 'white', }),
        ], className="twelve columns")
    ]),



    html.Div(children=[
        ################### Filter box ######################
        html.Div(children=[
            html.H4(children='Konfliktart vs Weltwirtschaft'),
            html.H6(children='Erklärung',
                    style={'marginTop': '-15px', 'marginBottom': '30px'}),
            html.P(children='Diese zwei Graphen zeigen das Verhältnis von globalen Konflikten zu weltwirtschaftlichen Kennzahlen.'),
            html.P(children='Der linke Graph unterteilt die Konfliktarten nach der Methodik vom Heidelberger Institut für Internationale Konfliktforschung (HIIK).'),
            html.P(children='Im oberen Dropdown wird die KPI ausgewählt und im unteren Dropdown wird die Konfliktart ausgewählt.'),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Label(children='Datenquellen: ',
                       style={'font-weight': 'bold'}),
            html.A(children='Konfliktarten nach HIIK',
                   href='https://de.statista.com/statistik/daten/studie/2736/umfrage/entwicklung-der-anzahl-von-konflikten-weltweit/', target="_blank"),
        ], className="two columns",
            style={'padding': '2rem', 'margin': '1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'marginTop': '2rem', 'background-color': 'white'}),


        html.Div(children=[
            # Line chart for accidents per day
            html.Div(children=[
                dcc.Dropdown(id='column_picker',
                             options=[
                                 {'label': 'West Texas Intermediate',
                                  'value': 'WTI (USD je Barrel)'},
                                 {'label': 'Brent',
                                     'value': 'UK Brent (USD je Barrel)'},
                             ],
                             optionHeight=35,  # height/space between dropdown options
                             # dropdown value selected automatically when page loads
                             value='WTI (USD je Barrel)',
                             disabled=False,  # disable dropdown value selection
                             multi=False,  # allow multiple dropdown values to be selected
                             searchable=True,  # allow user-searching of dropdown values
                             search_value='',  # remembers the value searched in dropdown
                             # gray, default text shown when no option is selected
                             placeholder='Please select...',
                             clearable=False,  # allow user to removes the selected value
                             # use dictionary to define CSS styles of your dropdown
                             style={'width': "50%",
                                    'display': 'inline-block'},
                             # className='select_box',           #activate separate CSS document in assets folder
                             # persistence=True,                 #remembers dropdown value. Used with persistence_type
                             # persistence_type='memory'         #remembers dropdown value selected until...
                             ),
                dcc.Dropdown(id='conflict_picker_two',
                             options=conflict_options[1:],
                             optionHeight=35,  # height/space between dropdown options
                             # dropdown value selected automatically when page loads
                             value='Gesamt',
                             disabled=False,  # disable dropdown value selection
                             multi=False,  # allow multiple dropdown values to be selected
                             searchable=True,  # allow user-searching of dropdown values
                             search_value='',  # remembers the value searched in dropdown
                             # gray, default text shown when no option is selected
                             placeholder='Please select...',
                             clearable=False,  # allow user to removes the selected value
                             # use dictionary to define CSS styles of your dropdown
                             style={'width': "50%"},
                             # className='select_box',           #activate separate CSS document in assets folder
                             # persistence=True,                 #remembers dropdown value. Used with persistence_type
                             # persistence_type='memory'         #remembers dropdown value selected until...
                             ),
                dcc.Graph(id='kip_world_graph'),
            ], className="five columns", style={'padding': '2rem', 'margin': '1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'marginTop': '2rem', 'backgroundColor': 'white'}),
            html.Div(children=[
                dcc.Dropdown(id='world_kip_picker',
                             options=testkip[1:],
                             style={'width': "47.8%", 'marginBottom': '.5rem'},
                             clearable=False,
                             placeholder='KPI auswählen..'
                             ),
                html.Div(children=[
                    dcc.Input(
                        id='textarea',
                        placeholder='Ihre Eingabe...', type='text'
                    )]),
                dcc.DatePickerSingle(
                    id='date-picker-single', style={'marginTop': '.5rem'},
                    date='2017-06-21',
                    display_format='DD.MM.YYYY'
                ),
                html.Button('submit',
                            id='submit',  style={'marginLeft': '.3rem'}),
                html.Button('clear',
                            id='clear',  style={'marginLeft': '.3rem'}),

                dcc.Graph(id='testgraph', figure=figgy)
            ], className="five columns", style={'padding': '2rem', 'margin': '1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'marginTop': '2rem', 'backgroundColor': 'white'})
        ])
    ], className="twelve columns"),
    html.Div(children=[
        ################### Filter box ######################
        html.Div(children=[
            html.H4(
                 children='Konfliktart vs Wirtschaft in den G8+5 Staaten'),
             html.H6(children='Erklärung',
                     style={'marginTop': '-15px', 'marginBottom': '30px'}),
             html.P(children='Dieser Graph zeigt die Anzahl der Google bzw. YouTube-Suchanfragen in einer jeweiligen Woche in Prozent zum höchsten Wert. 100 bedeutet, dass in dieser Woche die meisten Suchanfragen zu dieser Konfliktregion abgeschickt wurden.'),
             html.P(
                 children='Auf der rechten Seite können die jeweiligen Keyword ausgeblendet und eingeblendet werden.'),
             html.P(children='(DEU) steht für Suchanfragen aus Deutschland.'),
             html.P(children='(WLD) steht für weltweite Suchanfragen.'),
             html.Br(),
             html.Br(),
             html.Label(children='Datenquellen: ',
                        style={'font-weight': 'bold'}),
             html.A(children='Google-Trends',
                    href='https://www.google.com/trends', target="_blank"), ], className="two columns",
            style={'padding': '2rem', 'margin': '1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'marginTop': '2rem', 'background-color': 'white'}),

        ##### HERE insert the code for four boxes & graph #########
        html.Div(children=[
            # Line chart for accidents per day
            html.Div(children=[
                dcc.Dropdown(id='country_picker',
                             options=country_options,
                             optionHeight=35,  # height/space between dropdown options
                             value='Germany',  # dropdown value selected automatically when page loads
                             disabled=False,  # disable dropdown value selection
                             multi=False,  # allow multiple dropdown values to be selected
                             searchable=True,  # allow user-searching of dropdown values
                             search_value='',  # remembers the value searched in dropdown
                             # gray, default text shown when no option is selected
                             placeholder='Please select...',
                             clearable=False,  # allow user to removes the selected value
                             # use dictionary to define CSS styles of your dropdown
                             style={'width': "50%"},
                             # className='select_box',           #activate separate CSS document in assets folder
                             # persistence=True,                 #remembers dropdown value. Used with persistence_type
                             # persistence_type='memory'         #remembers dropdown value selected until...
                             ),
                dcc.Dropdown(id='kip_picker',
                             options=kip_options[3:],
                             optionHeight=35,  # height/space between dropdown options
                             # dropdown value selected automatically when page loads
                             value='BIP Wachstum zum Vorjahr in %',
                             disabled=False,  # disable dropdown value selection
                             multi=False,  # allow multiple dropdown values to be selected
                             searchable=True,  # allow user-searching of dropdown values
                             search_value='',  # remembers the value searched in dropdown
                             # gray, default text shown when no option is selected
                             placeholder='Please select...',
                             clearable=False,  # allow user to removes the selected value
                             # use dictionary to define CSS styles of your dropdown
                             style={'width': "50%"},
                             # className='select_box',           #activate separate CSS document in assets folder
                             # persistence=True,                 #remembers dropdown value. Used with persistence_type
                             # persistence_type='memory'         #remembers dropdown value selected until...
                             ),
                dcc.Dropdown(id='conflict_picker',
                             options=conflict_options[1:],
                             optionHeight=35,  # height/space between dropdown options
                             # dropdown value selected automatically when page loads
                             value='Gesamt',
                             disabled=False,  # disable dropdown value selection
                             multi=False,  # allow multiple dropdown values to be selected
                             searchable=True,  # allow user-searching of dropdown values
                             search_value='',  # remembers the value searched in dropdown
                             # gray, default text shown when no option is selected
                             placeholder='Please select...',
                             clearable=False,  # allow user to removes the selected value
                             # use dictionary to define CSS styles of your dropdown
                             style={'width': "50%"},
                             # className='select_box',           #activate separate CSS document in assets folder
                             # persistence=True,                 #remembers dropdown value. Used with persistence_type
                             # persistence_type='memory'         #remembers dropdown value selected until...
                             ),
                dcc.Graph(id='country_kip_graph'),
            ], className="five columns", style={'padding': '2rem', 'margin': '1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'marginTop': '2rem', 'backgroundColor': 'white', }),
        ])
    ], className="twelve columns"),
    html.Div(children=[
        ################### Filter box ######################
        html.Div(children=[
             html.H4(
                 children='Google Suchen nach Konfliktregion'),
             html.H6(children='Erklärung',
                     style={'marginTop': '-15px', 'marginBottom': '30px'}),
             html.P(children='Dieser Graph zeigt die Anzahl der Google-Suchanfragen in einer jeweiligen Woche in Prozent zum höchsten Wert. 100 bedeutet, dass in dieser Woche die meisten Suchanfragen zu dieser Konfliktregion abgeschickt wurden.'),
             html.P(
                 children='Auf der rechten Seite können die jeweiligen Keyword ausgeblendet und eingeblendet werden.'),
             html.P(children='(DEU) steht für Suchanfragen aus Deutschland'),
             html.P(children='(WLD) steht für weltweite Suchanfragen'),
             html.P(
                 children='Mit einem Klick auf den Button wechselt man zwischen Google- und YouTube-Suchanfragen.'),
             html.Br(),
             html.Br(),
             html.Label(children='Datenquellen: ',
                        style={'font-weight': 'bold'}),
             html.A(children='Google-Trends',
                    href='https://www.google.com/trends', target="_blank"),
             ], className="two columns",
            style={'padding': '2rem', 'margin': '1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'marginTop': '2rem', 'background-color': 'white'}),

        ##### HERE insert the code for four boxes & graph #########
        html.Div(children=[
            # Line chart for accidents per day
            html.Div(children=[
                html.Button('Toggle YouTube/Google',
                            id='toggle_yt_google_trends', n_clicks=0),
                dcc.Graph(id='google_trends_conflicts_graph',
                          figure=fig_google_trends_conflicts),
            ], className="five columns", style={'padding': '2rem', 'margin': '1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'marginTop': '2rem', 'backgroundColor': 'white', }),
            html.Div(children=[
                html.Button('Trendlinie on/off',
                            id='trendline_on_off', n_clicks=0),
                dcc.Graph(id='google_trends_afg_ukr'),
            ], className="five columns", style={'padding': '2rem', 'margin': '1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'marginTop': '2rem', 'backgroundColor': 'white', })

        ],
        )
    ], className="twelve columns"),


], style={'padding': '2rem'})


@app.callback(
    Output(component_id='testgraph',
           component_property='figure'),
    Input(component_id='submit', component_property='n_clicks'),
    Input(component_id='clear', component_property='n_clicks'),
    State(component_id='date-picker-single', component_property='date'),
    State(component_id='textarea', component_property='value'),
    State(component_id='testgraph', component_property='figure'),
    Input(component_id='world_kip_picker', component_property='value'),
)
def update_output_div(n_clicks, value, dates, conflict, fig, kip):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    figure = plotly.graph_objects.Figure(fig)

    if trigger_id == 'world_kip_picker':
        figure = px.line(testdata, x='year',
                         y=str(kip))
    else:
        if trigger_id == "submit":
            figure.add_vline(x=dt.datetime.strptime(dates, "%Y-%m-%d").timestamp() * 1000,
                             annotation_text=conflict,
                             line_width=3, line_dash="dash",
                             line_color="green")
        else:
            figure = copy.deepcopy(figgy)

    return figure


@app.callback(
    Output(component_id='google_trends_afg_ukr', component_property='figure'),
    [Input('trendline_on_off', 'n_clicks')],
)
def update_output_div(n_clicks):
    df = google_trends_afg_ukr_absolute

    if (n_clicks % 2) == 0:
        fig = px.scatter(
            df, x='week', y=df.columns, trendline='lowess', title="<b>Google-Trends</b> in Wochen", labels={
                'week': 'Woche',
                'value': '<b>Suchanfragen</b> in %',
                'variable': '<b>Konflikt</b><br>'
            })
    else:
        fig = px.scatter(
            df, x='week', y=df.columns, title="<b>Google-Trends</b> in Wochen", labels={
                'week': 'Woche',
                'value': '<b>Suchanfragen</b> in %',
                'variable': '<b>Konflikt</b><br>'
            })

    return fig


@app.callback(
    Output(component_id='google_trends_conflicts_graph',
           component_property='figure'),
    [Input('toggle_yt_google_trends', 'n_clicks')],
)
def update_output_div(n_clicks):

    if (n_clicks % 2) == 0:
        fig = fig_google_trends_conflicts
        fig.update_layout(title="<b>Google-Trends</b> in Wochen")
    else:
        fig = fig_yt_trends_conflicts
        fig.update_layout(title="<b>YouTube-Trends</b> in Wochen")
    return fig


@ app.callback(
    Output(component_id='country_kip_graph', component_property='figure'),
    Input(component_id='country_picker', component_property='value'),
    Input(component_id='kip_picker', component_property='value'),
    Input(component_id='conflict_picker', component_property='value'),
    # Input('my-range-slider', 'value')

)
def build_graph(country_chosen, kip_chosen, conflict_chosen):
    copy = bachelor_table
    dff = copy[copy['country_name'] == country_chosen]
    fig = make_subplots(specs=[[{"secondary_y": True}]])


# Add traces

    fig.add_trace(
        go.Bar(x=war_table['year'],
               y=war_table[conflict_chosen],
               name=str(conflict_chosen),
               opacity=0.5),
        secondary_y=True,

    )
    fig.add_trace(
        go.Scatter(x=dff['year'], y=dff[kip_chosen],
                   name=str(kip_chosen), mode='lines+markers'),
        secondary_y=False,
    )


# add dropdown menus to the figure


# Add figure title
    fig.update_layout(
        title_text="Verhältnis Konfliktart vs <b>" +
        str(kip_chosen)+"</b> in <b>"+str(country_chosen)+"</b>"
    )

# Set x-axis title
    fig.update_xaxes(title_text="Jahr", range=[2001, 2022])

# Set y-axes titles
    fig.update_yaxes(
        title_text='<b>primary</b> '+str(kip_chosen), secondary_y=False)
    fig.update_yaxes(
        title_text='<b>secondary</b> '+str(conflict_chosen), secondary_y=True)

    return fig


@app.callback(
    Output(component_id='kip_world_graph', component_property='figure'),
    Input(component_id='column_picker', component_property='value'),
    Input(component_id='conflict_picker_two', component_property='value')

)
def build_graph(column_chosen, conflict_chosen_two):
    df = oil_prices
    fig = make_subplots(specs=[[{"secondary_y": True}]])


# Add traces

    fig.add_trace(
        go.Bar(x=war_table['year'],
               y=war_table[conflict_chosen_two],
               name=str(conflict_chosen_two),
               opacity=0.5),
        secondary_y=True,

    )
    fig.add_trace(
        go.Scatter(x=df['year'], y=df[column_chosen],
                   name=str(column_chosen), mode='lines+markers'),
        secondary_y=False,
    )


# add dropdown menus to the figure


# Add figure title
    fig.update_layout(
        title_text="Verhältnis Konfliktart vs " +
        "<b>"+str(column_chosen)+"</b>"
    )

# Set x-axis title
    fig.update_xaxes(title_text="Jahr", range=[2001, 2022])

# Set y-axes titles
    fig.update_yaxes(
        title_text='<b>primary</b> '+str(column_chosen), secondary_y=False)
    fig.update_yaxes(
        title_text='<b>secondary</b> '+str(conflict_chosen_two), secondary_y=True)

    return fig


# app starter
if __name__ == "__main__":
    app.run_server(debug=True)

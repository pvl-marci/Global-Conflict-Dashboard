from re import template
from turtle import color
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
from plotly.subplots import make_subplots
import statsmodels.api as sm
from datetime import datetime as dt

# Dataframes
oil_prices = pd.read_csv('oil_brent_texas.csv', header=[0])
# KIP Ländertabelle
bachelor_table = pd.read_csv('bachelor_tablde.csv')
bachelor_table = bachelor_table.astype({'year': int})

# Einlesen der Konflikttabelle
war_table = pd.read_csv('war_table.csv')
war_table = war_table.astype({'year': int})

# Einlesen der Google Trends für Konflikte
google_trends_conflicts = pd.read_csv('conflicts_google_trends.csv')

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

# rename der Konflikttabellenköpfe       year,dispute,non_violent_crises,violent_crises,limited_wars,wars,total
war_table = war_table.rename(columns={
    'dispute': 'Dispute',
    'non_violent_crises': 'gewaltlose Kriege',
    'violent_crises': 'gewaltsame Kriege',
    'limited_wars': 'begrenzte Kriege',
    'wars': 'Kriege',
    'total': 'Gesamt',
})

# rename der KIP Tabellenköpfe
oil_prices = oil_prices.rename(columns={
    'price_texas': 'Preis West Texas Intermediate (je Barrel in USD)',
    'price_brent': 'Preis UK Brent (je Barrel in USD)',
})


# KIP Array für Dropdown
kip_options = []
for kip in bachelor_table:
    kip_options.append({'label': str(kip), 'value': kip})

'Country Array für Dropdown'
country_options = []
for country in bachelor_table['country_name'].unique():
    country_options.append({'label': str(country), 'value': country})

# Conflict Array für Dropdown
conflict_options = []
for conflict in war_table:
    conflict_options.append({'label': str(conflict), 'value': conflict})

# Figures

# GoogleTrendsConflicts
fig_google_trends_conflicts = px.scatter(
    google_trends_conflicts, x='week', y=google_trends_conflicts.columns)
fig_google_trends_conflicts.update_traces(mode='lines+markers')

fig_google_trends_conflicts.update_layout(
    title_text="<b>Google-Trends</b> in Wochen",
    template='plotly_white'
)
# create an app
app = Dash(__name__)

# applayout
app.layout = html.Div(children=[


    html.Div(children=[
        html.H3(children='global conflicts data'),
        html.H6(children='Bachelor Thesis 2022',
                style={'marginTop': '-20px', 'marginBottom': '30px'})
    ], style={'textAlign': 'center'}),



    html.Div(children=[
        ################### Filter box ######################
        html.Div(children=[
            html.H4(children='Das Verhältnis von Konfliktart auf die Weltwirtschaft'),
            html.H6(children='Erklärung',
                    style={'marginTop': '-15px', 'marginBottom': '30px'}),
            html.P(children='Diese zwei Graphen zeigen das Verhältnis von globalen Konflikten zu weltwirtschaftlichen Kennzahlen.'),
            html.P(children='Der linke Graph unterteilt die Konfliktarten nach der Methodik vom Heidelberger Institut für Internationale Konfliktforschung (HIIK).'),
            html.P(children='Im oberen Dropdown wird die KPI ausgewählt und im unteren Dropdown wird die Konfliktart ausgewählt.'),
            html.Br(),
            html.Br(),
            html.Label(children='Quellen: ', style={'font-weight': 'bold'}),
            html.A(children='Konfliktarten nach HIIK',
                   href='https://de.statista.com/statistik/daten/studie/2736/umfrage/entwicklung-der-anzahl-von-konflikten-weltweit/', target="_blank"),
        ], className="four columns",
            style={'padding': '2rem', 'margin': '1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'marginTop': '2rem', 'background-color': 'white'}),

        ##### HERE insert the code for four boxes & graph #########
        html.Div(children=[
            # Line chart for accidents per day
            html.Div(children=[
                dcc.Dropdown(id='column_picker',
                             options=[
                                 {'label': 'West Texas Intermediate',
                                     'value': 'Preis West Texas Intermediate (je Barrel in USD)'},
                                 {'label': 'Brent',
                                     'value': 'Preis UK Brent (je Barrel in USD)'},
                             ],
                             optionHeight=35,  # height/space between dropdown options
                             # dropdown value selected automatically when page loads
                             value='Preis West Texas Intermediate (je Barrel in USD)',
                             disabled=False,  # disable dropdown value selection
                             multi=False,  # allow multiple dropdown values to be selected
                             searchable=True,  # allow user-searching of dropdown values
                             search_value='',  # remembers the value searched in dropdown
                             # gray, default text shown when no option is selected
                             placeholder='Please select...',
                             clearable=False,  # allow user to removes the selected value
                             # use dictionary to define CSS styles of your dropdown
                             style={'width': "50%", 'display': 'inline-block'},
                             # className='select_box',           #activate separate CSS document in assets folder
                             # persistence=True,                 #remembers dropdown value. Used with persistence_type
                             # persistence_type='memory'         #remembers dropdown value selected until...
                             ),
                dcc.Dropdown(id='conflict_picker_two',
                             options=conflict_options,
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
            ], className="six columns", style={'padding': '2rem', 'margin': '1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'marginTop': '2rem', 'backgroundColor': 'white', }),
        ])
    ]),
    html.Div(children=[
        ################### Filter box ######################
        html.Div(children=[], className="four columns",
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
                             clearable=True,  # allow user to removes the selected value
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
                             clearable=True,  # allow user to removes the selected value
                             # use dictionary to define CSS styles of your dropdown
                             style={'width': "50%"},
                             # className='select_box',           #activate separate CSS document in assets folder
                             # persistence=True,                 #remembers dropdown value. Used with persistence_type
                             # persistence_type='memory'         #remembers dropdown value selected until...
                             ),
                dcc.Dropdown(id='conflict_picker',
                             options=conflict_options,
                             optionHeight=35,  # height/space between dropdown options
                             # dropdown value selected automatically when page loads
                             value='Gesamt',
                             disabled=False,  # disable dropdown value selection
                             multi=False,  # allow multiple dropdown values to be selected
                             searchable=True,  # allow user-searching of dropdown values
                             search_value='',  # remembers the value searched in dropdown
                             # gray, default text shown when no option is selected
                             placeholder='Please select...',
                             clearable=True,  # allow user to removes the selected value
                             # use dictionary to define CSS styles of your dropdown
                             style={'width': "50%"},
                             # className='select_box',           #activate separate CSS document in assets folder
                             # persistence=True,                 #remembers dropdown value. Used with persistence_type
                             # persistence_type='memory'         #remembers dropdown value selected until...
                             ),
             dcc.Graph(id='country_kip_graph'),
             ], className="six columns", style={'padding': '2rem', 'margin': '1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'marginTop': '2rem', 'backgroundColor': 'white', }),
        ])
    ]),
    html.Div(children=[
        ################### Filter box ######################
        html.Div(children=[], className="four columns",
                 style={'padding': '2rem', 'margin': '1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'marginTop': '2rem', 'background-color': 'white'}),

        ##### HERE insert the code for four boxes & graph #########
        html.Div(children=[
            # Line chart for accidents per day
            html.Div(children=[
             dcc.Graph(id='google_trends_conflicts_graph',
                       figure=fig_google_trends_conflicts),
             ], className="six columns", style={'padding': '2rem', 'margin': '1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'marginTop': '2rem', 'backgroundColor': 'white', }),
        ])
    ]),


], style={'padding': '2rem'})


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

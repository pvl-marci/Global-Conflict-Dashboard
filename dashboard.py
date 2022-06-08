# import required packages
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
from plotly.subplots import make_subplots
import statsmodels.api as sm


nato_spendings = pd.read_csv('nato_spendings_2021.csv')
oil_prices = pd.read_csv('oil_brent_texas.csv')

# Einlesen der KIP Tabelle
bachelor_table = pd.read_csv('bachelor_tablde.csv')

# Einelsen der Konflikttabelle
war_table = pd.read_csv('war_table.csv')

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

kip_options = []
for kip in bachelor_table:
    kip_options.append({'label': str(kip), 'value': kip})

country_options = []
for country in bachelor_table['country_name'].unique():
    country_options.append({'label': str(country), 'value': country})

conflict_options = []
for conflict in war_table:
    conflict_options.append({'label': str(conflict), 'value': conflict})

app = Dash(__name__)


fig_nato_spendings = px.line(
    nato_spendings, x="year", y="spendings", color="country", labels={
        "spendings": "Militärausgaben in Millionen US-Dollar",
        "year": "Jahr",
        "country": "Land"
    })


to_plot = [v for v in list(oil_prices.columns) if v.startswith('price')]

fig_oil_prices = px.scatter(oil_prices, x='year', y=to_plot, trendline="lowess", labels={
    "value": "US-Dollar je Barrel",
    "year": "Jahr",
    "variable": "Öl Marke",
    "price_texas": "Texas"
})


fig_nato_spendings.update_layout(
    title_text="Ölpreisentwicklung"
)

fig_nato_spendings.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=3,
                     label="3y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)
fig_oil_prices.update_layout(
    title_text="Ölpreisentwicklung"
)

fig_oil_prices.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=3,
                     label="3y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)

app.layout = html.Div(className='row', children=[
    html.H1("Dashboard: Influence of military conflicts"),


    html.Div([
        html.H1('Hello Dash'),
        html.Div([
            html.P('Dash converts Python classes into HTML'),
            html.P(
                "This conversion happens behind the scenes by Dash's JavaScript front-end")
        ])
    ], ),



    html.Div(children=[
        dcc.Graph(id="graph1",  figure=fig_nato_spendings,
                  style={'display': 'inline-block'}),
        dcc.Graph(id="graph2", figure=fig_nato_spendings,
                  style={'display': 'inline-block'})
    ], ),
    html.Div(children=[
        dcc.Graph(id="graph3",  figure=fig_oil_prices,
                  style={'display': 'inline-block'}),
        dcc.Graph(id="graph4", figure=fig_oil_prices,
                  style={'display': 'inline-block'})
    ],),

    html.Div(children=[
        html.Div([
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
             dcc.Graph(id='our_graph', style={'width': "50%"})
             ],),

    ],),












])


@app.callback(
    Output(component_id='our_graph', component_property='figure'),
    Input(component_id='country_picker', component_property='value'),
    Input(component_id='kip_picker', component_property='value'),
    Input(component_id='conflict_picker', component_property='value'),

)
def build_graph(country_chosen, kip_chosen, conflict_chosen):
    copy = bachelor_table
    dff = copy[copy['country_name'] == country_chosen]
    fig = make_subplots(specs=[[{"secondary_y": True}]])


# Add traces
    fig.add_trace(
        go.Scatter(x=dff['year'], y=dff[kip_chosen],
                   name="Militärausgaben in UsSD", mode='lines+markers'),
        secondary_y=False,
    )

    fig.add_trace(
        go.Bar(x=war_table['year'],
               y=war_table[conflict_chosen],
               visible=True,
               name=str(conflict_chosen)),
        secondary_y=True,

    )


# add dropdown menus to the figure


# Add figure title
    fig.update_layout(
        title_text="Double Y Axis Example"
    )

# Set x-axis title
    fig.update_xaxes(title_text="Jahr")

# Set y-axes titles
    fig.update_yaxes(
        title_text='<b>primary</b> '+str(kip_chosen), secondary_y=False)
    fig.update_yaxes(
        title_text='<b>secondary</b> '+str(conflict_chosen), secondary_y=True)

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)

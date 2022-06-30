# import required packages
from re import template
from turtle import color
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
from plotly.subplots import make_subplots
import statsmodels.api as sm


nato_spendings = pd.read_csv('nato_spendings_2021.csv')
oil_prices = pd.read_csv('oil_brent_texas.csv', header=[0])

# Einlesen der KIP Tabelle
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

theme = {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}


fig_google_trends_conflicts = px.scatter(
    google_trends_conflicts, x='week', y=google_trends_conflicts.columns)
fig_google_trends_conflicts.update_traces(mode='lines+markers')

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

app.layout = html.Div(children=[
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

    html.Div(style={'width': "50%"}, children=[
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
                         options=conflict_options[2:],
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
             dcc.Graph(id='our_graph', style={'width': "100%"}),
             dcc.RangeSlider(
                id='my-range-slider',  # any name you'd like to give it
                marks={
                    2004: '2004',
                    2005: {'label': '2005', 'style': {'color': '#f50', 'font-weight': 'bold'}},
                    2006: '2006',
                    2008: '2008',
                    2010: '2010',
                    2012: '2012',
                    2014: '2014',
                    2016: '2016',
                    2018: '2018',
                    2020: '2020',
                    2021: '2021',
                },
                step=1,                # number of steps between values
                min=2004,
                max=2021,
                value=[2004, 2005],     # default value initially chosen
                dots=True,             # True, False - insert dots, only when step>1
                allowCross=False,      # True,False - Manage handle crossover
                disabled=False,        # True,False - disable handle
                pushable=2,            # any number, or True with multiple handles
                updatemode='mouseup',  # 'mouseup', 'drag' - update value method
                included=True,         # True, False - highlight handle
                vertical=False,        # True, False - vertical, horizontal slider
                # hight of slider (pixels) when vertical=True
                verticalHeight=900,
                className='None',
                tooltip={'always_visible': False,  # show current slider values
                         'placement': 'bottom'},
            ),
        ],),

    ],),


    html.Div(style={'width': "100%"}, children=[
        html.Div([
            dcc.Dropdown(id='column_picker',
                         options=[
                            {'label': 'Texas', 'value': 'price_texas'},
                            {'label': 'Brent', 'value': 'price_brent'},
                         ],
                         optionHeight=35,  # height/space between dropdown options
                         # dropdown value selected automatically when page loads
                         value='price_texas',
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
             dcc.Graph(id='our_graph_two', style={
                       'width': "100%", 'display': 'inline-block'}),
             ],),

    ],),

    html.Div(children=[
        dcc.Graph(id="graph5",  figure=fig_google_trends_conflicts)
    ], ),












])


@app.callback(
    Output(component_id='our_graph', component_property='figure'),
    Input(component_id='country_picker', component_property='value'),
    Input(component_id='kip_picker', component_property='value'),
    Input(component_id='conflict_picker', component_property='value'),
    #Input('my-range-slider', 'value')

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
        title_text="Verhältnis Krieg vs <b>" +
        str(kip_chosen)+"</b> in <b>"+str(country_chosen)+"</b>"
    )

# Set x-axis title
    fig.update_xaxes(title_text="Jahr", range=[2000, 2022])

# Set y-axes titles
    fig.update_yaxes(
        title_text='<b>primary</b> '+str(kip_chosen), secondary_y=False)
    fig.update_yaxes(
        title_text='<b>secondary</b> '+str(conflict_chosen), secondary_y=True)

    return fig


@app.callback(
    Output(component_id='our_graph_two', component_property='figure'),
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
        title_text="Verhältnis Krieg vs " + "<b>"+str(column_chosen)+"</b>",
        template='plotly_dark'
    )

# Set x-axis title
    fig.update_xaxes(title_text="Jahr", range=[2001, 2022])

# Set y-axes titles
    fig.update_yaxes(
        title_text='<b>primary</b> '+str(column_chosen), secondary_y=False)
    fig.update_yaxes(
        title_text='<b>secondary</b> '+str(conflict_chosen_two), secondary_y=True)

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)

  
import numpy
import pandas as pd
from datetime import datetime as dt

import plotly
import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)

## This date is Johns Hopkins University which can be downloaded here: https://github.com/CSSEGISandData/COVID-19

df = pd.read_csv("./data/deaths.csv")
print(df[:5])

mark_values={0: 0,              # key=position, value=what you see
             5: 5,
             10: 10,
             15: 15,
             20: 20,
             25: 25,
             50: 50,
             75: 75,
             100: {'label': 100, 'style': {'color':'#f50', 'font-weight':'bold'}},
             125: 125,
             150: 150}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.Div([
        dcc.Graph(id='our_graph')
    ],className='nine columns'),
        
    html.Div([
        html.Br(),
        html.Label(['Choose Up to 6 Countries to Compare:'],style={'font-weight': 'bold', "text-align": "center"}),
        dcc.Dropdown(id='country_one',
            options=[{'label':x, 'value':x} for x in df.sort_values('Country')['Country'].unique()],
            value='US',
            multi=False,
            disabled=False,
            clearable=True,
            searchable=True,
            placeholder='Choose Country...',
            className='form-dropdown',
            style={'width':"90%"},
            persistence='string',
            persistence_type='memory'),

        dcc.Dropdown(id='country_two',
            options=[{'label':x, 'value':x} for x in df.sort_values('Country')['Country'].unique()],
            value='Brazil',
            multi=False,
            clearable=False,
            persistence='string',
            persistence_type='memory'),

        dcc.Dropdown(id='country_three',
            options=[{'label':x, 'value':x} for x in df.sort_values('Country')['Country'].unique()],
            value='United Kingdom',
            multi=False,
            clearable=False,
            persistence='string',
            persistence_type='memory'),

        dcc.Dropdown(id='country_four',
            options=[{'label':x, 'value':x} for x in df.sort_values('Country')['Country'].unique()],
            value='Spain',
            multi=False,
            clearable=False,
            persistence='string',
            persistence_type='memory'),

        dcc.Dropdown(id='country_five',
            options=[{'label':x, 'value':x} for x in df.sort_values('Country')['Country'].unique()],
            value='Italy',
            multi=False,
            clearable=False,
            persistence='string',
            persistence_type='memory'),

        dcc.Dropdown(id='country_six',
            options=[{'label':x, 'value':x} for x in df.sort_values('Country')['Country'].unique()],
            value='China',
            multi=False,
            clearable=False,
            persistence='string',
            persistence_type='memory'),

    ],className='three columns'),

    html.Div([
        html.Label(['Choose range of days since 10th total confirmed death: '],
                    style={'font-weight': 'bold'}),
        html.P(),
        dcc.RangeSlider(
            id='the_days',  # any name you'd like to give it
            step=1,                # number of steps between values
            min=0,
            max=160,
            value=[0,50],          # default value initially chosen
            marks=mark_values,
            dots=True,             # True, False - insert dots, only when step>1
            allowCross=False,      # True,False - Manage handle crossover
            disabled=False,        # True,False - disable handle
            pushable=2,            # any number, or True with multiple handles
            updatemode='mouseup',  # 'mouseup', 'drag' - update value method
            included=True,         # True, False - highlight handle
            vertical=False,        # True, False - vertical, horizontal slider
            verticalHeight=900,    # hight of slider (pixels) when vertical=True
            className='None',
            tooltip={'always visible':False,  # show current slider values
                     'placement':'bottom'}
        ),
    ],className='twelve columns'),

    dcc.Markdown(('''

    Data and chart last updated: March 20, 23:00 GMT


    ##### Author
    * [@eddwebster](https://www.twitter.com/eddwebster)
    * [eddwebster.com](https://www.eddwebster.com/)
    * [GitHub/eddwebster](https://github.com/eddwebster/). All code available [here](https://github.com/eddwebster/covid-19)
    

    ##### Sources and References
    * [FT's Corona Virus Tracker](https://www.ft.com/content/a26fbf7e-48f8-11ea-aeb3-955839e06441) by [John Burn-Murdoch](https://twitter.com/jburnmurdoc) 
    * [COVID-19 GitHub Data Repository](https://github.com/CSSEGISandData/COVID-19) by the [Center for Systems Science and Engineering (CSSE) at John Hopkins University](https://coronavirus.jhu.edu/)
    * [Coronavirus Pandemic Data Explorer](https://ourworldindata.org/coronavirus) by [Our World in Data](https://ourworldindata.org/)
    * [European Centre for Disease Prevention and Control](https://www.ecdc.europa.eu/en/geographical-distribution-2019-ncov-cases)
    * [Worldometers's Corona Virus Tracker](https://www.worldometers.info/coronavirus/)
    '''),className='twelve columns')
    
])
  

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components 
@app.callback(
    Output('our_graph','figure'),
    [Input('country_one','value'),
     Input('country_two','value'),
     Input('country_three','value'),
     Input('country_four','value'),
     Input('country_five','value'),
     Input('country_six','value'),
     Input('the_days', 'value')]
)

def build_graph(first_country, second_country, third_country, forth_country, fifth_country, sixth_country, days_chosen):
    
    dff=df[(df['Days_Since_First_10_Deaths']>=days_chosen[0])&
           (df['Days_Since_First_10_Deaths']<=days_chosen[1])&
           ((df['Country']==first_country)|
            (df['Country']==second_country)|
            (df['Country']==third_country)|
            (df['Country']==forth_country)|
            (df['Country']==fifth_country)|
            (df['Country']==sixth_country))]
    # print(dff[:5])

    fig = px.line(dff,
                  x="Days_Since_First_10_Deaths",
                  y="Deaths",
                  color='Country',
                  log_y=True,
                 #range_x=(0, 160),
                  range_y=(10, 200_000),
                  height=600)
    fig.update_layout(xaxis={'title':'Number of days since 10th total confirmed death'},
                      yaxis={'title':'Total Deaths'},
                      title={'text':'Country by country: how coronavirus death trajectories compare',
                      'font':{'size':28},'x':0.5,'xanchor':'center'})
    
    fig.update_traces(textposition='top center')
    
    return fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=False)
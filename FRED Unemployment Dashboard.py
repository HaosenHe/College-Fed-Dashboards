# @Haosen He 2020
from fredapi import Fred
import datetime
import chart_studio.plotly as py
import plotly.graph_objs as go
import numpy as np
import pandas as pd
from copy import deepcopy
import dash
import dash_core_components as dcc
import dash_html_components as html

fred = Fred(api_key='1e447a08c4fbfd495098d0747c38f3af') 
# This api key should only be used for WFU 2020 College Fed Chanllenge Team Python Dahsboard
# Do not use this key for other purposes

#load series
y = fred.get_series('GDPC1')['2020-01-01':]
#cpi=fred.get_series('CPIAUCSL')['2020-01-01':]
unrate=fred.get_series('UNRATE')['2020-01-01':]
lfpr=fred.get_series("CIVPART")['2020-01-01':]
#rate=fred.get_series("INTDSRUSM193N")['2020-01-01':]
iniclaim=fred.get_series("ICSA")['2020-01-01':]
contclaim=fred.get_series("CCSA")['2020-01-01':]
#m1=fred.get_series("M1")['2020-01-01':]

x1=iniclaim.index
x2=contclaim.index
all_claim=deepcopy(contclaim)
for i in range(0,len(all_claim)):
    all_claim[i]=all_claim[i]+iniclaim[i]

app=dash.Dash()
app.layout = html.Div(children=[
    html.H1('U.S. Unemployment Indicators from St. Louis Fed'),
    html.H2('A Naive Python Dashboard'),
    html.H3("@Haosen He 2020"),
    dcc.Graph(id='unclaim',
              figure = {
                'data': [{'x':x1, 'y' : iniclaim, 'name' : 'Initial Claim'},
                         {'x':x1, 'y' : contclaim, 'name' : 'Continued Claim'},
                         {'x':x1, 'y' : all_claim, 'name' : 'Total Claim'}
                        ],
                  'layout': {
                      'title' : 'U.S. Unemployment Claims'
                  }
              }),
    dcc.Graph(id='unrate',
              figure = {
                'data': [{'x': unrate.index, 'y' : unrate}],
                'layout': {
                'title' : 'U.S. Unemployment Rate'
                  }
              }),
    dcc.Graph(id='lfpr',
              figure = {
                'data': [{'x': lfpr.index, 'y' : lfpr}],
                'layout': {
                'title' : 'U.S. Labor Force Participation Rate'
                  }
              })
 ])   
    

if __name__ =='__main__':
    app.run_server(debug=False, use_reloader=False,threaded=True)
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


#balance sheet
# (WALCL)
#Assets: Total Assets: Total Assets (Less Eliminations From Consolidation): Wednesday Level (WALCL)
#Assets: Other: Repurchase Agreements: Wednesday Level (WORAL)
#Assets: Securities Held Outright: U.S. Treasury Securities: All: Wednesday Level (TREAST)
#Assets: Securities Held Outright: Mortgage-Backed Securities: Wednesday Level (WSHOMCB)
#Assets: Central Bank Liquidity Swaps: Central Bank Liquidity Swaps: Wednesday Level (SWPT)
total=fred.get_series('WALCL')['2007-01-01':]
ustreasury=fred.get_series('TREAST')['2007-01-01':]
mbs=fred.get_series('WSHOMCB')['2007-01-01':]
repo=fred.get_series('WORAL')['2007-01-01':]

x=total.index
x1=iniclaim.index
x2=contclaim.index
all_claim=deepcopy(contclaim)
for i in range(0,len(all_claim)):
    all_claim[i]=all_claim[i]+iniclaim[i]
    
# Balance Sheet
bsheet = go.Figure()
bsheet.add_trace(go.Scatter(
    x=x, y=total,
    name = 'Others',
    hoverinfo='name+x+y',
    line=dict(color='red'),
    fillcolor='rgba(255,0,0,1)',
    fill='tonexty'
    ))
bsheet.add_trace(go.Scatter(
    x=x, y=mbs,
    hoverinfo='name+x+y',
    name = 'Mortagage-Backed Securities',
    line=dict(color='forestgreen'),
    fillcolor='rgba(34,139,34,1)',
    mode='none',
    stackgroup='one'
))

bsheet.add_trace(go.Scatter(
    x=x, y=repo,
    hoverinfo='name+x+y',
    name = 'Repurchase Agreements',
    line=dict(color='darkorange'),
    fillcolor='rgba(255,140,0,1)',
    mode='none',
    stackgroup='one'
))

bsheet.add_trace(go.Scatter(
    x=x, y=ustreasury,
    hoverinfo='name+x+y',
    name = 'U.S.Treasury Bill',
    line=dict(color='dodgerblue'),
    fillcolor='rgba(0,128,255,1)',
    stackgroup='one' # define stack group
))

bsheet.update_layout(
    title="Federal Reserve Balance Sheet: Assets",
    title_x=0.5
)

app=dash.Dash()
app.layout = html.Div(children=[
    html.H1('U.S. Economic Indicators from St. Louis Fed'),
    html.H2('Python Dashboard'),
   # html.H3("@Haosen He 2020"),
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
    
    dcc.Graph(figure=bsheet),
          
    dcc.Graph(id='unrate_and_lfpr',
              figure = {
                'data': [{'x': x1, 'y' : unrate, 'name' : 'Unemployment Rate'},
                         {'x': x1, 'y' : lfpr, 'name' : 'Labor Force Participation Rate'}
                         ],
                'layout': {
                'title' : 'U.S. Unemployment and Labor Force Participation Rates'
                  }
              })
    ])

if __name__ =='__main__':
    app.run_server(debug=False, use_reloader=False,threaded=True)

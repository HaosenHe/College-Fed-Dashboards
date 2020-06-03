# @Haosen He 2020
from fredapi import Fred
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import dash
from copy import deepcopy
import dash_core_components as dcc
import dash_html_components as html
from urllib.request import urlopen
import json
with open("C:\\Users\\s1760\\Desktop\\CFC\\WFU CFC Dashboard\\state_hash.json", "r") as read_file:
    geodata = json.load(read_file)

fred = Fred(api_key='1e447a08c4fbfd495098d0747c38f3af')
# This api key should only be used for WFU 2020 College Fed Chanllenge Team Python Dahsboard
# Do not use this key for other purposes

#load series
y = fred.get_series('GDPC1')['2020-01-01':]
#cpi=fred.get_series('CPIAUCSL')['2020-01-01':]
unrate=fred.get_series('UNRATE')['2020-01-01':]
lfpr=fred.get_series("CIVPART")['2020-01-01':]

#rates
ffr=fred.get_series("DFF")['2020-01-01':]
threemtreasure=fred.get_series('DTB3')['2020-01-01':]
tenyrtreasure=fred.get_series('DGS10')['2020-01-01':]
libor=fred.get_series('USD1MTD156N')['2020-01-01':]
oneyrtreasure=fred.get_series('DGS1')['2020-01-01':]

iniclaim=fred.get_series("ICSA")['2020-01-01':]
contclaim=fred.get_series("CCSA")['2020-01-01':]

mb=fred.get_series('BOGMBASEW')['2007-01-01':]
m1=fred.get_series("M1")['2007-01-01':]
m2=fred.get_series("M2")['2007-01-01':]

mb=[x/1000 for x in mb]
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
x3=ffr.index
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

msheet = go.Figure()
msheet.add_trace(go.Scatter(
    x=m1.index, y=m2,
    name = 'M2',
    hoverinfo='name+x+y',
    line=dict(color='red'),
    fillcolor='rgba(255,0,0,1)',
    fill='tonexty'
    ))
msheet.add_trace(go.Scatter(
    x=m1.index, y=m1,
    hoverinfo='name+x+y',
    name = 'M1',
    line=dict(color='forestgreen'),
    fillcolor='rgba(34,139,34,1)',
    mode='none',
    stackgroup='one'
))
msheet.add_trace(go.Scatter(
    x=m1.index, y=mb,
    hoverinfo='name+x+y',
    name = 'Monetary Base',
    line=dict(color='darkorange'),
    fillcolor='rgba(255,140,0,1)',
    mode='none',
    stackgroup='one'
))

msheet.update_layout(
    title="Monetary Base, M1 and M2 in the U.S.",
    title_x=0.5
)

#continued claims Choropleth
state_code=['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN',
            'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH',
            'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT',
            'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
cclaims=[]
for i in state_code:
    cclaims.append(fred.get_series(i+"CCLAIMS")[-1]/(fred.get_series(i+"POP")[-1]*1000))

dfdict={'state_code':state_code, 'cclaims':cclaims}
df=pd.DataFrame(dfdict)

cclaimsmap = px.choropleth(df, geojson=geodata,
                           locations="state_code", scope='usa',
                           color='cclaims',
                           labels={'cclaims':'continued claims/state population'})

cclaimsmap.update_layout(title="Number of Continued Claims as Percentages of State Population",
                         title_x=0.5)
cclaimsmap.update_layout(
    autosize=False,
    width=1000,
    height=800,)

app=dash.Dash()
app.layout = html.Div(children=[
    html.H1('U.S. Economic Indicators from St. Louis Fed'),
    html.H2('Python Dashboard'),
    # html.H3("@Haosen He 2020"),

    dcc.Graph(figure=cclaimsmap),

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

    dcc.Graph(id='rates',
              figure = {
                'data': [{'x': x3, 'y' : ffr, 'name' : 'Effective Federal Funds Rate'},
                         {'x': x3, 'y' : libor, 'name' : 'LIBOR'},
                         {'x': x3, 'y' : threemtreasure, 'name' : '3-Month Treasury Bill: Secondary Market Rate'},
                         {'x': x3, 'y' : oneyrtreasure, 'name' : '1-Year Treasury Constant Maturity Rate'},
                         {'x': x3, 'y' : tenyrtreasure, 'name' : '10-Year Treasury Constant Maturity Rate'}
                         ],
                'layout': {
                'title' : 'Short-term Interest Rates and T-Bill Returns'
                  }
              }),

    dcc.Graph(figure=msheet),


    ])


if __name__ =='__main__':
    app.run_server(debug=False, use_reloader=False,threaded=True)

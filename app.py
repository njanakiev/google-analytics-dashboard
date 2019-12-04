import os
import utils
import numpy as np
import pandas as pd
from datetime import datetime
import flask
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)
#app = dash.Dash(__name__, server=server,
#                routes_pathname_prefix='/',
#                requests_pathname_prefix='/dashboard/')


KEY_FILE_LOCATION = os.environ['KEY_FILE_LOCATION']
VIEW_ID = os.environ['VIEW_ID']
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']


def load_data():
    df = utils.ga_dataframe(KEY_FILE_LOCATION, SCOPES, body={
    'reportRequests': [{
        'viewId': VIEW_ID,
        'dateRanges': [{'startDate': '2017-01-01', 'endDate': 'yesterday'}],
        'metrics': [
            {"expression": "ga:pageviews"}
        ], "dimensions": [
            {"name": "ga:date"},
            #{"name": "ga:sourceMedium"},
            {"name": "ga:pagePath"}
        ], "samplingLevel": "LARGE",
        "pageSize": 10000
    }]})

    df['ga:date'] = pd.to_datetime(df['ga:date'])
    df.set_index('ga:date', inplace=True)

    df['ga:pagePath'] = df['ga:pagePath'].str.replace('/til/', '/blog/')
    df = df.groupby(['ga:date', 'ga:pagePath']).sum()
    df = df.reset_index().set_index('ga:date')

    df = df.reset_index().pivot(index='ga:date',
        columns='ga:pagePath', values='ga:pageviews')
    columns = df.sum().sort_values(ascending=False).index.values
    df = df[columns]
    df.index = pd.to_datetime(df.index)
    df.insert(0, 'total', df.sum(axis=1))

    return df


def create_figure(df):
    columns = df.columns[:50]

    data = [go.Scatter(x=df.index,
                       y=df[col],
                       name=col,
                       visible=i==0) for i, col in enumerate(columns)]

    buttons = []
    for i, col in enumerate(columns):
        visible = np.zeros(len(columns), dtype=bool)
        visible[i] = True
        buttons.append(dict(label=col,
                            method='update',
                            args=[dict(visible=visible)]))

    updatemenus = [dict(buttons=buttons,
                        direction='down',
                        xanchor='left',
                        yanchor='bottom')]

    layout = dict(height=600, updatemenus=updatemenus)

    return go.Figure(data=data, layout=layout)


df = load_data()

app.layout = html.Div(children=[
    html.H2('GA Dashboard'),
    html.Div(className='row', children=[
        dcc.Graph(id='views', figure=create_figure(df))
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)

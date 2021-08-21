import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly as py
import plotly.tools as tls
import plotly.graph_objects as go
from plotly import offline
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import os
import base64
from loader_covid import Loader_Covid


matplotlib.use('agg')

#function to get plotly figures from mpl figures in order to use them in the dashboard
def get_plotly_figure(mpl_axes, costum_xlabels=False):
    mpl_axes.get_legend().remove()
    fig = mpl_axes.get_figure()
    x_labels = [tick.get_text() for tick in mpl_axes.get_xticklabels()[1:-1]]
    x_positions = [pos for pos in mpl_axes.get_xticks()[1:-1]]
    plotly_fig = tls.mpl_to_plotly(fig)
    plotly_legend = go.layout.Legend()
    if costum_xlabels:
        plotly_fig.update_xaxes(rangeslider_visible=True, tickvals=x_positions, ticktext=x_labels)
    else:
        plotly_fig.update_xaxes(rangeslider_visible=True)
    plotly_fig.update_layout(showlegend=True, legend=plotly_legend, autosize=True)
    return plotly_fig

#statistics studied
covid_infos = ['cases', 'deaths', 'recovered']

#locations studied
locations = [['United States', 'Florida', 'Miami-Dade County'],
             ['Germany', 'Bavaria', ''],
             ['Brazil', '', ''],
             ['Worldwide', '', '']]

loader = Loader_Covid(True)
loader.plot_world_map()
loader.load(locations)

###PLOTS FOR TAB 1 (Used data)
plots_used = loader.plots()
Miami_plot = get_plotly_figure(plots_used[0]).update_layout(autosize = False, width = 750, height = 750, margin=dict(t=60, b=30, l=0, r=0))
Bayern_plot = get_plotly_figure(plots_used[1]).update_layout(autosize = False, width = 750, height = 750, margin=dict(t=60, b=30, l=0, r=0))
Brazil_plot = get_plotly_figure(plots_used[2]).update_layout(autosize = False, width = 750, height = 750, margin=dict(t=60, b=30, l=0, r=0))
World_plot = get_plotly_figure(plots_used[3]).update_layout(autosize = False, width = 750, height = 750, margin=dict(t=60, b=30, l=0, r=0))

###PLOTS FOR TAB 2 (Prediction)

#Confirmed
loader.split_data(target = 'Confirmed')
plots_pred_confirmed = loader.forecasting()
loader.diagnostics()
Miami_pred_confirmed = get_plotly_figure(plots_pred_confirmed[0]).update_layout(autosize = False, width = 750, height = 750, margin=dict(t=60, b=30, l=0, r=0))
Miami_pred = Miami_pred_confirmed
Bayern_pred_confirmed = get_plotly_figure(plots_pred_confirmed[1]).update_layout(autosize = False, width = 750, height = 750, margin=dict(t=60, b=30, l=0, r=0))
Bayern_pred = Bayern_pred_confirmed
Brazil_pred_confirmed = get_plotly_figure(plots_pred_confirmed[2]).update_layout(autosize = False, width = 750, height = 750, margin=dict(t=60, b=30, l=0, r=0))
Brazil_pred = Brazil_pred_confirmed
World_pred_confirmed = get_plotly_figure(plots_pred_confirmed[3]).update_layout(autosize = False, width = 750, height = 750, margin=dict(t=60, b=30, l=0, r=0))
World_pred = World_pred_confirmed


#Deaths
loader.split_data(target = 'Deaths')
plots_pred_deaths = loader.forecasting()
loader.diagnostics()
Miami_pred_deaths = get_plotly_figure(plots_pred_deaths[0]).update_layout(autosize = False, width = 750, height = 750, margin=dict(t=60, b=30, l=0, r=0))
Bayern_pred_deaths = get_plotly_figure(plots_pred_deaths[1]).update_layout(autosize = False, width = 750, height = 750, margin=dict(t=60, b=30, l=0, r=0))
Brazil_pred_deaths = get_plotly_figure(plots_pred_deaths[2]).update_layout(autosize = False, width = 750, height = 750, margin=dict(t=60, b=30, l=0, r=0))
World_pred_deaths = get_plotly_figure(plots_pred_deaths[3]).update_layout(autosize = False, width = 750, height = 750, margin=dict(t=60, b=30, l=0, r=0))


#Confirmed NO DATA FROM MIAMI AND BAYERN
loader.split_data(target = 'Recovered')
plots_pred_recovered = loader.forecasting()
loader.diagnostics()
Brazil_pred_recovered = get_plotly_figure(plots_pred_recovered[2]).update_layout(autosize = False, width = 750, height = 750, margin=dict(t=60, b=30, l=0, r=0))
World_pred_recovered = get_plotly_figure(plots_pred_recovered[3]).update_layout(autosize = False, width = 750, height = 750, margin=dict(t=60, b=30, l=0, r=0))


#DASHBOARD CODE

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

colors = {
    'background': '#FFFFFF',
    'text': '#000000'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='COVID prediction',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    dcc.Tabs([
        dcc.Tab(label='Used data', children=[#First tab plotting used data for the project
            html.Div(style={'backgroundColor': colors['background'], 'width': 'auto', 'float': 'left', 'margin': '20px'}, children=[
                html.H2(#Maps representing covid impact
                    children='Global COVID Maps',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),
                html.Label('Information Type'),
                dcc.RadioItems(
                    id='covid_worldmap-type',
                    options=[{'label': i, 'value': i} for i in covid_infos],
                    value='cases',
                    labelStyle={'display': 'block', 'padding': '1px 10px', 'white-space':'normal'}
                ),
                html.Div([
                    html.Img(id='covid_worldmap')
                ])
            ]),
            html.Div(style={'backgroundColor': colors['background'], 'width': 'auto', 'float': 'left', 'margin': '20px'}, children=[
                html.H2(
                    children='World COVID Data',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),
                html.Div([
                    dcc.Graph(id='World_plot', figure=World_plot)
                
                ]),
            ]),
            html.Div(style={'backgroundColor': colors['background'], 'width': 'auto', 'float': 'left', 'margin': '20px'}, children=[
                html.H2(
                    children='Brazil COVID Data',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),
                html.Div([
                    dcc.Graph(id='Brazil_plot', figure=Brazil_plot)
                
                ]),
            ]),
            html.Div(style={'backgroundColor': colors['background'], 'width': 'auto', 'float': 'left', 'margin': '20px'}, children=[
                html.H2(
                    children='Bavaria COVID Data',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),
                html.Div([
                    dcc.Graph(id='Bayern_plot', figure=Bayern_plot)
                
                ]),
            ]),
            html.Div(style={'backgroundColor': colors['background'], 'width': 'auto', 'float': 'left', 'margin': '20px'}, children=[
                html.H2(
                    children='Miami COVID Data',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),
                html.Div([
                    dcc.Graph(id='Miami_plot', figure=Miami_plot)
                
                ]),
            ])
        ]),
        dcc.Tab(label='Prediction', children=[#Second tab where we show the predictions made with SARIMA
            html.Div(style={'backgroundColor': colors['background'], 'width': 'auto', 'float': 'left', 'margin': '20px'}, children=[
                html.H2(
                    children='World COVID Prediction',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),

                html.Label('Prediction Target'),
                dcc.RadioItems(
                    id='world-type',
                    options=[
                        {'label': 'Confirmed', 'value': 'Confirmed'},
                        {'label': 'Deaths', 'value': 'Deaths'},
                        {'label': 'Recovered', 'value': 'Recovered'}],
                    value='Confirmed',
                    labelStyle={'display': 'inline-block', 'padding': '1px 10px'}
                ),

                html.Div([
                    dcc.Graph(id='World_pred', figure=World_pred)
                
                ]),
            ]),

            html.Div(style={'backgroundColor': colors['background'], 'width': 'auto', 'float': 'left', 'margin': '20px'}, children=[
                html.H2(
                    children='Brazil COVID Prediction',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),

                html.Label('Prediction Target'),
                dcc.RadioItems(
                    id='brazil-type',
                    options=[
                        {'label': 'Confirmed', 'value': 'Confirmed'},
                        {'label': 'Deaths', 'value': 'Deaths'},
                        {'label': 'Recovered', 'value': 'Recovered'}],
                    value='Confirmed',
                    labelStyle={'display': 'inline-block', 'padding': '1px 10px'}
                ),

                html.Div([
                    dcc.Graph(id='Brazil_pred', figure=Brazil_pred)
                
                ]),
            ]),

            html.Div(style={'backgroundColor': colors['background'], 'width': 'auto', 'float': 'left', 'margin': '20px'}, children=[
                html.H2(
                    children='Bavaria COVID Prediction',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),

                html.Label('Prediction Target'),
                dcc.RadioItems(
                    id='bayern-type',
                    options=[
                        {'label': 'Confirmed', 'value': 'Confirmed'},
                        {'label': 'Deaths', 'value': 'Deaths'}],
                    value='Confirmed',
                    labelStyle={'display': 'inline-block', 'padding': '1px 10px'}
                ),

                html.Div([
                    dcc.Graph(id='Bayern_pred', figure=Brazil_pred)
                
                ]),
            ]),

            html.Div(style={'backgroundColor': colors['background'], 'width': 'auto', 'float': 'left', 'margin': '20px'}, children=[
                html.H2(
                    children='Miami COVID Prediction',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),

                html.Label('Prediction Target'),
                dcc.RadioItems(
                    id='miami-type',
                    options=[
                        {'label': 'Confirmed', 'value': 'Confirmed'},
                        {'label': 'Deaths', 'value': 'Deaths'}],
                    value='Confirmed',
                    labelStyle={'display': 'inline-block', 'padding': '1px 10px'}
                ),

                html.Div([
                    dcc.Graph(id='Miami_pred', figure=Miami_pred)
                
                ]),
            ])
        ]),
        dcc.Tab(label='Diagnostics', children=[#Third tab showing the diagnosis of our predictions
            html.Div(style={'backgroundColor': colors['background'], 'width': 'auto', 'float': 'left', 'margin': '20px'}, children=[
                html.H2(
                    children='World COVID Prediction Diagnostics',
                    style={
                        'textAlign': 'left',
                        'color': colors['text']
                    }
                ),

                html.Label('Prediction Target'),
                dcc.RadioItems(
                    id='world_diagnostics-type',
                    options=[
                        {'label': 'Confirmed', 'value': 'Confirmed'},
                        {'label': 'Deaths', 'value': 'Deaths'},
                        {'label': 'Recovered', 'value': 'Recovered'}],
                    value='Confirmed',
                    labelStyle={'display': 'inline-block', 'padding': '1px 10px'}
                ),

                html.Div([
                    html.Img(id='world_diagnostics')
                
                ])
            ]),

            html.Div(style={'backgroundColor': colors['background'], 'width': 'auto', 'float': 'left', 'margin': '20px'}, children=[
                html.H2(
                    children='Brazil COVID Prediction Diagnostics',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),

                html.Label('Prediction Target'),
                dcc.RadioItems(
                    id='brazil_diagnostics-type',
                    options=[
                        {'label': 'Confirmed', 'value': 'Confirmed'},
                        {'label': 'Deaths', 'value': 'Deaths'},
                        {'label': 'Recovered', 'value': 'Recovered'}],
                    value='Confirmed',
                    labelStyle={'display': 'inline-block', 'padding': '1px 10px'}
                ),

                html.Div([
                    html.Img(id='brazil_diagnostics')
                
                ]),
            ]),
            html.Div(style={'backgroundColor': colors['background'], 'width': 'auto', 'float': 'left', 'margin': '20px'}, children=[
                html.H2(
                    children='Bayern COVID Prediction Diagnostics',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),

                html.Label('Prediction Target'),
                dcc.RadioItems(
                    id='bayern_diagnostics-type',
                    options=[
                        {'label': 'Confirmed', 'value': 'Confirmed'},
                        {'label': 'Deaths', 'value': 'Deaths'}],
                    value='Confirmed',
                    labelStyle={'display': 'inline-block', 'padding': '1px 10px'}
                ),

                html.Div([
                    html.Img(id='bayern_diagnostics')
                
                ]),
            ]),

            html.Div(style={'backgroundColor': colors['background'], 'width': 'auto', 'float': 'left', 'margin': '20px'}, children=[
                html.H2(
                    children='Miami COVID Prediction Diagnostics',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),

                html.Label('Prediction Target'),
                dcc.RadioItems(
                    id='miami_diagnostics-type',
                    options=[
                        {'label': 'Confirmed', 'value': 'Confirmed'},
                        {'label': 'Deaths', 'value': 'Deaths'}],
                    value='Confirmed',
                    labelStyle={'display': 'inline-block', 'padding': '1px 10px'}
                ),

                html.Div([
                    html.Img(id='miami_diagnostics')
                
                ]),
            ])
        ])
    ])
])

###CALLBACKS needed to have a dynamic dashboard
# Bing Covid Worldmap
@app.callback(
    Output('covid_worldmap', 'src'),
    [Input('covid_worldmap-type', 'value')])
def update_covid_worldmap_src(info):
    image_path = '../plots/' + info + '.png'
    encoded_image = base64.b64encode(open(image_path, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded_image.decode())

#World prediction
@app.callback(
    Output('World_pred', 'figure'),
    [Input('world-type', 'value')])
def update_world_prediction(target):
    if target == 'Confirmed':
        plot = World_pred_confirmed
    if target == 'Deaths':
        plot = World_pred_deaths
    if target == 'Recovered':
        plot = World_pred_recovered
    return plot

#Brazil prediction
@app.callback(
    Output('Brazil_pred', 'figure'),
    [Input('brazil-type', 'value')])
def update_brazil_prediction(target):
    if target == 'Confirmed':
        plot = Brazil_pred_confirmed
    if target == 'Deaths':
        plot = Brazil_pred_deaths
    if target == 'Recovered':
        plot = Brazil_pred_recovered
    return plot

#Bayern prediction
@app.callback(
    Output('Bayern_pred', 'figure'),
    [Input('bayern-type', 'value')])
def update_bayern_prediction(target):
    if target == 'Confirmed':
        plot = Bayern_pred_confirmed
    if target == 'Deaths':
        plot = Bayern_pred_deaths
    return plot

#Miami prediction
@app.callback(
    Output('Miami_pred', 'figure'),
    [Input('miami-type', 'value')])
def update_miami_prediction(target):
    if target == 'Confirmed':
        plot = Miami_pred_confirmed
    if target == 'Deaths':
        plot = Miami_pred_deaths
    return plot

#World diagnostics
@app.callback(
    Output('world_diagnostics', 'src'),
    [Input('world_diagnostics-type', 'value')])
def update_covid_worldmap_src(target):
    image_path = '../plots/Worldwide_' + target + '_diag.png'
    encoded_image = base64.b64encode(open(image_path, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded_image.decode())

#Brazil diagnostics
@app.callback(
    Output('brazil_diagnostics', 'src'),
    [Input('brazil_diagnostics-type', 'value')])
def update_covid_worldmap_src(target):
    image_path = '../plots/Brazil_' + target + '_diag.png'
    encoded_image = base64.b64encode(open(image_path, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded_image.decode())

#Bayern diagnostics
@app.callback(
    Output('bayern_diagnostics', 'src'),
    [Input('bayern_diagnostics-type', 'value')])
def update_covid_worldmap_src(target):
    image_path = '../plots/Germany, Bavaria_' + target + '_diag.png'
    encoded_image = base64.b64encode(open(image_path, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded_image.decode())

#Miami diagnostics
@app.callback(
    Output('miami_diagnostics', 'src'),
    [Input('miami_diagnostics-type', 'value')])
def update_covid_worldmap_src(target):
    image_path = '../plots/United States, Florida, Miami-Dade County_' + target + '_diag.png'
    encoded_image = base64.b64encode(open(image_path, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded_image.decode())


if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_ui=False, dev_tools_props_check=False)
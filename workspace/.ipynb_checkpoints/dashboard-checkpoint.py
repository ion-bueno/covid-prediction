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
from main import Loader_Covid


matplotlib.use('agg')

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


covid_infos = ['cases', 'deaths', 'recovered']

loader = Loader_Covid()
locations = [['Spain', 'Madrid', ''], 
            ['Germany', 'Bavaria', ''],
            ['Worldwide', '', '']]
loader.load(locations)

#plots for Tab 1
plots_used = loader.plots()
Madrid_plot = get_plotly_figure(plots_used[0]).update_layout(autosize = False, width = 750, height = 750, margin=dict(t=60, b=30, l=0, r=0))
Bayern_plot = get_plotly_figure(plots_used[1]).update_layout(autosize = False, width = 750, height = 750, margin=dict(t=60, b=30, l=0, r=0))
World_plot = get_plotly_figure(plots_used[2])

#plots for Tab2
loader.split_data()
plots_pred = loader.forecasting()
Madrid_pred = get_plotly_figure(plots_pred[0])
Bayern_pred = get_plotly_figure(plots_pred[1]).update_layout(autosize = False, width = 750, height = 750, margin=dict(t=60, b=30, l=0, r=0))
World_pred = get_plotly_figure(plots_pred[2]).update_layout(autosize = False, width = 750, height = 750, margin=dict(t=60, b=30, l=0, r=0))

#dashboard

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
        dcc.Tab(label='Used data', children=[
            html.Div(style={'backgroundColor': colors['background'], 'width': 'auto', 'float': 'left', 'margin': '20px'}, children=[
                html.H2(
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
                    children='Madrid COVID Data',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),
                html.Div([
                    dcc.Graph(id='Madrid_plot', figure=Madrid_plot)
                
                ]),
            ])
        ]),
        dcc.Tab(label='Prediction', children=[
            html.Div(style={'backgroundColor': colors['background'], 'width': 'auto', 'float': 'left', 'margin': '20px'}, children=[
                html.H2(
                    children='World COVID Prediction',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),
                html.Div([
                    dcc.Graph(id='World_pred', figure=World_pred)
                
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
                html.Div([
                    dcc.Graph(id='Bayern_pred', figure=Bayern_pred)
                
                ]),
            ]),
            html.Div(style={'backgroundColor': colors['background'], 'width': 'auto', 'float': 'left', 'margin': '20px'}, children=[
                html.H2(
                    children='Madrid COVID Prediction',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),
                html.Div([
                    dcc.Graph(id='Madrid_pred', figure=Madrid_pred)
                
                ]),
            ])
        ])
    ])
])

#Callbacks
# Bing Covid Worldmap
@app.callback(
    Output('covid_worldmap', 'src'),
    [Input('covid_worldmap-type', 'value')])
def update_covid_worldmap_src(info):
    image_path = './plots/' + info + '.png'
    encoded_image = base64.b64encode(open(image_path, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded_image.decode())

if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_ui=False, dev_tools_props_check=False)







    
'''
data = pd.read_csv('https://raw.githubusercontent.com/microsoft/Bing-COVID-19-Data/master/data/Bing-COVID19-Data.csv' 
                    if online else 'bing_covid.csv', index_col='ID')
if online:
    data.to_csv('bing_covid.csv')
    
current_data = self.data.drop_duplicates(
            subset=['ISO2', 'ISO3', 'Country_Region', 'AdminRegion1', 'AdminRegion2'], keep='last')
countries: pd.DataFrame = current_data.drop_duplicates(subset=['ISO3'], keep='first').iloc[1:]

drawn_series = pd.Series([0]*len(countries['ISO3']), index=countries['ISO3'])
cmap = mpl.cm.cool
norm = mpl.colors.Normalize(
            vmin=drawn_series.min(), vmax=drawn_series.max())

iso3_colors = drawn_series.map(lambda x: cmap(norm(x)))

shapename = 'admin_0_countries'
countries_shp = shpreader.natural_earth(resolution='110m',
                    category='cultural', name=shapename)

fig = plt.figure(figsize=(9,9))
ax = plt.axes(projection=ccrs.PlateCarree())
fig.add_axes(ax)
ax.coastlines()
label = {
    'cases': 'Number of cases',
    'case rate': 'Number of cases per 100k people',
    'case change': 'Number of new cases in the last day',
    'deaths': 'Number of deaths',
    'death rate': 'Number of deaths per 100k people',
    'death change': 'Number of deaths in the last day',
    'recovered': 'Number of recovered people',
    'recovered rate': 'Number of recovered people per 100k people',
    'recovered change': 'Number of recoveries in the last day'
}[data_to_draw]

fig.colorbar(mpl.cm.ScalarMappable(
    norm=norm, cmap=cmap), label=label, orientation='horizontal')

for country in shpreader.Reader(countries_shp).records():
    try:
        ax.add_geometries([country.geometry], ccrs.PlateCarree(),
                          facecolor=iso3_colors[country.attributes['ISO_A3']],
                          label=country.attributes['NAME_LONG'])
    except:
        pass
'''


# Group: Daniel Martín Cruz, Ion Bueno Ulacia

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy
import cartopy.io.shapereader as shpreader
from cartopy import crs as ccrs
import auto_arima_model as model
import warnings
warnings.filterwarnings("ignore")


class Loader_Covid():
    # Initialization of the object
    def __init__(self, online=False): #online = True if you want the updated database from internet
        url = 'https://raw.githubusercontent.com/microsoft/Bing-COVID-19-Data/master/data/Bing-COVID19-Data.csv'
        self.data = pd.read_csv(url if online else 'bing_covid.csv', index_col='ID')
        if online: #selecting True the stored database gets updated
            self.data.to_csv('bing_covid.csv')
        self.dict = {}
        self.splitted_dict = {}
        self.locations = []
        self.models = {}
        self.target = None
        
    # Data source and loading whole locations
    def load(self, locations): 
        for location in locations:
            conditions = (self.data['Country_Region']==location[0]) & \
                         (self.data['AdminRegion1']==location[1] if location[1]!='' else self.data['AdminRegion1'].isna()) & \
                         (self.data['AdminRegion2']==location[2] if location[2]!='' else self.data['AdminRegion2'].isna())
            df = self.data[conditions]
            df = df.drop(columns=['ConfirmedChange', 'DeathsChange', 'RecoveredChange',
                                      'Latitude', 'Longitude', 'ISO2', 'ISO3',
                                      'AdminRegion1', 'AdminRegion2', 'Country_Region'])
            df = df.set_index('Updated')
            df.index = pd.to_datetime(df.index)
            df = df.fillna(0) #filling NaN values with zeros
            key = location[0]
            if location[1] != '':
                key += ', ' + location[1]
                if location[2] != '':
                    key += ', ' + location[2] 
            self.dict[key] = df
            self.locations = list(self.dict.keys())
        return self.dict
        
    # Data visualization of locations
    def plots(self):
        axes = []
        for location in self.dict: 
            ax = self.dict[location][['Confirmed', 'Deaths', 'Recovered']].plot(figsize = (10, 6))
            fig = ax.get_figure()
            axes.append(ax)
            plt.xlabel('Date')
            plt.ylabel('Cases')
            plt.title(f'Confirmed, Deaths and Recovered in {location}')
        return axes
    
    # Train and test sets for each location
    def split_data(self, test_split=0.25, target='Confirmed'):
        self.target = target
        self.splitted_dict = {}
        for location in self.dict:
            df = self.dict[location]
            index = round(len(df) * (1 - test_split))
            X_train = df[:index]
            X_test = df[index:]
            train = X_train[target]
            test = X_test[target]
            self.splitted_dict[location] = {'train': train, 'test':test}
        return self.splitted_dict
    
    # Prediction
    def forecasting(self, steps=None): #None means forecast=test
        axes = []
        for location in self.splitted_dict:
            automodel = model.auto_arima(self.splitted_dict[location]['train'])
            self.models[location] = automodel
            ax = model.plot_auto_arima(self.splitted_dict[location]['train'], self.splitted_dict[location]['test'], automodel, steps, location)
            axes.append(ax)
        return axes
    
    # Residual plots
    def diagnostics(self):
        figures = []
        for location in self.splitted_dict:
            if self.splitted_dict[location]['train'][-1] == 0:
                pass
            else:
                fig = model.diagnostics_auto_arima(self.models[location], location, self.target)
                figures.append(fig)
        return figures
        
        
    # Data visualization of the whole worlwide as a map
    def world_map(self, data_to_draw: str = 'cases') -> plt.Figure:
        if data_to_draw not in ['cases', 'deaths', 'recovered']:
            raise ValueError(
                'Unexpected value for data_to_draw: ' + str(data_to_draw))

        current_data = self.data.drop_duplicates(
            subset=['ISO2', 'ISO3', 'Country_Region', 'AdminRegion1', 'AdminRegion2'], keep='last')
        countries: pd.DataFrame = current_data.drop_duplicates(
            subset=['ISO3'], keep='first').iloc[1:]

        drawn_series = pd.Series(
            [0]*len(countries['ISO3']), index=countries['ISO3'])
        cmap = mpl.cm.cool

        if data_to_draw == 'cases':
            drawn_series = countries.set_index('ISO3')['Confirmed']
            cmap = mpl.cm.Greens
        elif data_to_draw == 'deaths':
            drawn_series = countries.set_index('ISO3')['Deaths']
            cmap = mpl.cm.Reds
        elif data_to_draw == 'recovered':
            drawn_series = countries.set_index('ISO3')['Recovered']
            cmap = mpl.cm.Blues

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
            'deaths': 'Number of deaths',
            'recovered': 'Number of recovered people'
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
        return fig
    
    # Plot of the map
    def plot_world_map(self, info_types=['cases', 'deaths', 'recovered']):
        for info_type in info_types:
            self.world_map(info_type).savefig('../plots/' + info_type + '.png', bbox_inches='tight')
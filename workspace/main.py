

# Group: Daniel Martín Cruz, Ion Bueno Ulacia

import loader_covid as ldr
import matplotlib.pyplot as plt

# Global visualization
ldr.Loader_Covid(True).plot_world_map() #it updates dataset

# New loader & locations
loader = ldr.Loader_Covid()
locations = [['United States', 'Florida', 'Miami-Dade County'],
             ['Brazil', '', ''],
             ['Germany', 'Bavaria', ''],
             ['Worldwide', '', '']] #[Country_Region, AdminRegion1, AdminRegion2]

# Data loading
data_dict = loader.load(locations)
loader.plots()


# 3 different targets to model
for target in ['Confirmed', 'Deaths', 'Recovered']:
    # Data forecasting
    data_split_dict = loader.split_data(target=target) #test_split
    loader.forecasting() #steps = future prediction

    # Diagnostics of residuals
    loader.diagnostics()
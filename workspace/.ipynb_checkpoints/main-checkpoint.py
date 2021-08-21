

# Group: Daniel Martín Cruz, Ion Bueno Ulacia

import loader_covid as ldr

# Global visualization
ldr.Loader_Covid(True).plot_world_map() #it updates dataset

# New loader & locations
loader = ldr.Loader_Covid()
locations = [['Spain', '', ''],
             ['Brazil', '', ''],
             ['Germany', 'Bavaria', ''],
             ['Worldwide', '', '']] #[Country_Region, AdminRegion1, AdminRegion2]

# Data loading
data_dict = loader.load(locations)
loader.plots()

# Data forecasting
data_split_dict = loader.split_data(target='Confirmed') #test_split, target: Confirmed, Deaths, Recovered
loader.forecasting() #steps = future prediction

# Diagnostics of residuals
loader.diagnostics()
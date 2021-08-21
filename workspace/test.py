from loader_covid import Loader_Covid
from matplotlib import pyplot as plt

data = Loader_Covid()
locations = ['Worldwide', '', '']
data.load(locations)
data.split_data(target = 'Confirmed')
data.split_data(target = 'Deaths')
plot = data.forecasting()
plt.show()
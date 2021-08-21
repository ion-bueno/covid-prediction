

# Group: Daniel Martín Cruz, Ion Bueno Ulacia

import pmdarima as pm
import pandas as pd
import matplotlib.pyplot as plt


def auto_arima(train, start_p=1, start_q=1, test='adf'):
    automodel = pm.auto_arima(train, 
                              start_p=start_p, 
                              start_q=start_q,
                              test=test,
                              seasonal=False,
                              trace=False,
                              error_action="ignore")
    return automodel

def plot_auto_arima(train, test, automodel, steps, location):
    if steps is None:
        steps = len(test)
    # Forecast
    fc, confint = automodel.predict(n_periods=steps, return_conf_int=True)
    # Weekly index
    fc_ind = pd.date_range(train.index[train.shape[0]-1], periods=steps)
    # Forecast series
    fc_series = pd.Series(fc, index=fc_ind)   
    aux_df = pd.DataFrame({'Training': train, 'Test': test, 'Forecast': fc_series})
    # Create plot
    plt.figure()
    ax = aux_df.plot(figsize=(10, 6))
    plt.xlabel('Date')
    plt.ylabel(train.name)
    plt.legend(("Training", "Test", "Forecast"), loc="upper left")
    plt.title(f'AUTO-ARIMA model in {location} for {train.name} cases')
    return ax



def diagnostics_auto_arima(automodel, location, target):
    fig = plt.figure()
    ax = automodel.plot_diagnostics(figsize=(10,6))
    plt.suptitle(f'Residual plots for AUTO-ARIMA model in {location} for {target} cases')
    return ax
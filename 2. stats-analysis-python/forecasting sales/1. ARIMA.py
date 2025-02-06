# 1. Dependencies
import pandas as pd
import numpy as np
import math
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 2. Load Dataset
def load_data(file_path):
    """Load dataset from the given file path."""
    data = pd.read_excel(file_path)
    data['Sales'] = pd.to_numeric(data['Sales'], errors='coerce')
    return data['Sales'].dropna()  # Ensure no missing values for analysis

# 3. Logarithm Transformation
def apply_log_transformation(series):
    """Apply logarithmic transformation to the series."""
    return series.apply(lambda x: math.log(x) if x > 0 else None)

# 4. Stationarity Test
def adf_test(series):
    """Perform the Augmented Dickey-Fuller (ADF) test for stationarity."""
    result = adfuller(series)
    print(f"ADF Statistic: {result[0]}")
    print(f"p-value: {result[1]}")
    return result[1] < 0.05  # Stationary if p-value < 0.05

def kpss_test(series):
    """Perform the Kwiatkowski-Phillips-Schmidt-Shin (KPSS) test for stationarity."""
    result = kpss(series, regression='c')
    print(f"KPSS Statistic: {result[0]}")
    print(f"p-value: {result[1]}")
    return result[1] > 0.05  # Stationary if p-value > 0.05

# 5. ACF and PACF Plot
def plot_acf_pacf(series):
    """Plot ACF and PACF for the time series."""
    fig = make_subplots(rows=1, cols=2, subplot_titles=("ACF", "PACF"))

    acf_values = sm.tsa.stattools.acf(series, nlags=20)
    fig.add_trace(go.Bar(x=list(range(len(acf_values))), y=acf_values), row=1, col=1)

    pacf_values = sm.tsa.stattools.pacf(series, nlags=20)
    fig.add_trace(go.Bar(x=list(range(len(pacf_values))), y=pacf_values), row=1, col=2)

    fig.update_layout(title_text="ACF and PACF Plots", template="plotly_dark")
    fig.show()

# 6. Test Stationarity and Autocorrelation
def test_stationarity_and_autocorrelation(series):
    """Test for stationarity and plot autocorrelation functions."""
    if adf_test(series) and kpss_test(series):
        print("Series is stationary.")
        plot_acf_pacf(series)
        return True
    else:
        print("Series is non-stationary.")
        return False

# 7. Build ARIMA Model
def fit_arima_model(series, order):
    """Fit an ARIMA model to the series."""
    model = sm.tsa.ARIMA(series, order=order).fit()
    print(model.summary())
    return model

# 8. Main ARIMA Model Process
def arima_model(series):
    """Main ARIMA modeling process: Check stationarity, apply differencing if needed, and fit AR or MA model."""
    if not test_stationarity_and_autocorrelation(series):
        differenced_series = series.diff().dropna()
        print("Applied differencing.")
        
        if test_stationarity_and_autocorrelation(differenced_series):
            print("Fitting AR model on differenced series.")
            return fit_arima_model(differenced_series, order=(1, 0, 0))
        else:
            print("Differenced series is still non-stationary.")
            print("Fitting ARMA model on differenced series.")
            return fit_arima_model(differenced_series, order=(1, 0, 1))
    else:
        print("Fitting AR model on original series.")
        model_ar = fit_arima_model(series, order=(1, 0, 0))
        
        if not test_stationarity_and_autocorrelation(model_ar.resid):
            print("Autocorrelation present in residuals. Fitting MA model.")
            return fit_arima_model(series, order=(1, 0, 1))
        else:
            print("No autocorrelation in AR model residuals.")
            return model_ar

# 9. Execute the ARIMA process
def main(file_path):
    """Main function to execute the time series analysis and ARIMA modeling."""
    series = load_data(file_path)
    series = apply_log_transformation(series)  # Apply log transformation
    resulting_model = arima_model(series)
    return resulting_model

# Run the main workflow
if __name__ == "__main__":
    file_path = 'C:\\Users\\loydt\\Downloads\\Projects\\Superstore Sales Dataset.xlsx'
    model = main(file_path)

"""
ADF Statistic: -68.4498114214115
p-value: 0.0
KPSS Statistic: 0.07649061258135344
p-value: 0.1
C:\Users\loydt\AppData\Local\Temp\ipykernel_15936\1139732235.py:30: InterpolationWarning:

The test statistic is outside of the range of p-values available in the
look-up table. The actual p-value is greater than the p-value returned.


Series is stationary.
                               SARIMAX Results                                
==============================================================================
Dep. Variable:                  Sales   No. Observations:                 9800
Model:                 ARIMA(1, 0, 0)   Log Likelihood              -18788.007
Date:                Wed, 30 Oct 2024   AIC                          37582.014
Time:                        20:47:10   BIC                          37603.584
Sample:                             0   HQIC                         37589.323
                               - 9800                                         
Covariance Type:                  opg                                         
==============================================================================
                 coef    std err          z      P>|z|      [0.025      0.975]
------------------------------------------------------------------------------
const          4.1111      0.017    240.792      0.000       4.078       4.145
ar.L1          0.0142      0.010      1.415      0.157      -0.005       0.034
sigma2         2.7085      0.046     58.994      0.000       2.619       2.799
===================================================================================
Ljung-Box (L1) (Q):                   0.00   Jarque-Bera (JB):               178.58
Prob(Q):                              0.98   Prob(JB):                         0.00
Heteroskedasticity (H):               0.99   Skew:                             0.19
Prob(H) (two-sided):                  0.88   Kurtosis:                         2.46
===================================================================================

Warnings:
[1] Covariance matrix calculated using the outer product of gradients (complex-step).
ADF Statistic: -68.95774979092295
p-value: 0.0
KPSS Statistic: 0.07625561044700856
p-value: 0.1
C:\Users\loydt\AppData\Local\Temp\ipykernel_15936\1139732235.py:30: InterpolationWarning:

The test statistic is outside of the range of p-values available in the
look-up table. The actual p-value is greater than the p-value returned.


Series is stationary.
No autocorrelation in AR model residuals.
"""

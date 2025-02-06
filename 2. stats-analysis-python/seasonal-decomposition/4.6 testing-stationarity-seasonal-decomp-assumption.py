import pandas as pd
import numpy as np
import math
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, kpss
import warnings

# Suppress specific warnings for KPSS
warnings.filterwarnings("ignore", category=UserWarning, message="The test statistic is outside of the range of p-values available in the look-up table.")

# Function to load and preprocess dataset
def load_and_preprocess_data(file_path):
    data = pd.read_excel(file_path)
    data['Order Date'] = pd.to_datetime(data['Order Date'], errors='coerce')
    data.set_index('Order Date', inplace=True)
    return data

# Function to apply logarithmic transformation for stationarity testing
def log_transform_sales(monthly_sales):
    return monthly_sales.apply(lambda x: math.log(x) if x > 0 else None).dropna()

# Function to perform ADF and KPSS tests for stationarity and autocorrelation
def test_stationarity_and_autocorrelation(series, sub_category):
    # Perform ADF Test
    adf_result = adfuller(series)
    print(f"\nSub-Category: {sub_category}")
    print("ADF Test:")
    print(f"  ADF Statistic: {adf_result[0]}")
    print(f"  p-value: {adf_result[1]}")
    
    # Perform KPSS Test
    kpss_result = kpss(series, regression='c')
    print("\nKPSS Test:")
    print(f"  KPSS Statistic: {kpss_result[0]}")
    print(f"  p-value: {kpss_result[1]}")

# Function to process each sub-category
def process_sub_category(data, sub_category):
    # Filter data for the current sub-category
    sub_category_data = data[data['Sub-Category'] == sub_category]
    
    # Aggregate sales by month
    monthly_sales = sub_category_data['Sales'].resample('ME').sum()
    
    # Apply logarithmic transformation for stationarity testing
    transformed_sales = log_transform_sales(monthly_sales)
    
    # Perform stationarity tests if there is sufficient data
    if len(transformed_sales) > 0:
        test_stationarity_and_autocorrelation(transformed_sales, sub_category)

# Main function to run the entire process
def main():
    file_path = 'C:\\Users\\loydt\\Downloads\\Projects\\Superstore Sales Dataset.xlsx'
    data = load_and_preprocess_data(file_path)
    
    sub_categories = [
        'Bookcases', 'Chairs', 'Labels', 'Tables', 'Storage', 'Furnishings',
        'Art', 'Phones', 'Binders', 'Appliances', 'Paper', 'Accessories',
        'Envelopes', 'Fasteners', 'Supplies', 'Machines', 'Copiers'
    ]
    
    for sub_category in sub_categories:
        process_sub_category(data, sub_category)

# Run the main function
if __name__ == "__main__":
    main()


"""
Sub-Category: Bookcases
ADF Test:
  ADF Statistic: -6.027134171995194
  p-value: 1.446920160127645e-07

KPSS Test:
  KPSS Statistic: 0.26257551393839756
  p-value: 0.1

Sub-Category: Chairs
ADF Test:
  ADF Statistic: -6.197659232292192
  p-value: 5.911326600428518e-08

KPSS Test:
  KPSS Statistic: 0.4162803438561973
  p-value: 0.07013778282060462

Sub-Category: Labels
ADF Test:
  ADF Statistic: -5.182598245492526
  p-value: 9.540530724034473e-06

KPSS Test:
  KPSS Statistic: 0.21972387687240708
  p-value: 0.1

Sub-Category: Tables
ADF Test:
  ADF Statistic: -2.5114700477055205
  p-value: 0.11270842284915639

KPSS Test:
  KPSS Statistic: 0.40354771286030183
  p-value: 0.0756259858360768

Sub-Category: Storage
ADF Test:
  ADF Statistic: -0.1061438024383304
  p-value: 0.9488231382203466

KPSS Test:
  KPSS Statistic: 0.7388013844100835
  p-value: 0.010018055962719683

Sub-Category: Furnishings
ADF Test:
  ADF Statistic: -5.266380938270393
  p-value: 6.425515681850899e-06

KPSS Test:
  KPSS Statistic: 0.8617193246044281
  p-value: 0.01

Sub-Category: Art
ADF Test:
  ADF Statistic: -6.390210340838372
  p-value: 2.1150652220621213e-08

KPSS Test:
  KPSS Statistic: 0.6938602021335966
  p-value: 0.014103617987854858

Sub-Category: Phones
ADF Test:
  ADF Statistic: -5.076738094712931
  p-value: 1.5610147082484966e-05

KPSS Test:
  KPSS Statistic: 0.5881990252383348
  p-value: 0.023709179523787746

Sub-Category: Binders
ADF Test:
  ADF Statistic: -2.8091038506256187
  p-value: 0.056985069003992445

KPSS Test:
  KPSS Statistic: 0.5228996947473248
  p-value: 0.036509077759611534

Sub-Category: Appliances
ADF Test:
  ADF Statistic: -1.7791141444811294
  p-value: 0.39087912568754163

KPSS Test:
  KPSS Statistic: 0.9201046515890245
  p-value: 0.01

Sub-Category: Paper
ADF Test:
  ADF Statistic: -4.7073476267185095
  p-value: 8.151853566879724e-05

KPSS Test:
  KPSS Statistic: 0.8692539759187766
  p-value: 0.01

Sub-Category: Accessories
ADF Test:
  ADF Statistic: -4.680296044815936
  p-value: 9.16251904499705e-05

KPSS Test:
  KPSS Statistic: 0.8399131505029214
  p-value: 0.01

Sub-Category: Envelopes
ADF Test:
  ADF Statistic: -6.240940394087012
  p-value: 4.699103085589444e-08

KPSS Test:
  KPSS Statistic: 0.07920566757658486
  p-value: 0.1

Sub-Category: Fasteners
ADF Test:
  ADF Statistic: -3.5873309245959457
  p-value: 0.0060079038947011935

KPSS Test:
  KPSS Statistic: 0.334490090212803
  p-value: 0.1

Sub-Category: Supplies
ADF Test:
  ADF Statistic: -7.02833094890563
  p-value: 6.279466044516866e-10

KPSS Test:
  KPSS Statistic: 0.3716957110457206
  p-value: 0.08935529696305147

Sub-Category: Machines
ADF Test:
  ADF Statistic: -7.635837855099642
  p-value: 1.9535761462182718e-11

KPSS Test:
  KPSS Statistic: 0.08076812398741313
  p-value: 0.1

Sub-Category: Copiers
ADF Test:
  ADF Statistic: -5.058219250054243
  p-value: 1.700025710622307e-05

KPSS Test:
  KPSS Statistic: 0.3988750027508357
  p-value: 0.0776400850211915
C:\Users\loydt\AppData\Local\Temp\ipykernel_16620\4141645899.py:35: InterpolationWarning: The test statistic is outside of the range of p-values available in the
look-up table. The actual p-value is greater than the p-value returned.

  kpss_result = kpss(series, regression='c')
C:\Users\loydt\AppData\Local\Temp\ipykernel_16620\4141645899.py:35: InterpolationWarning: The test statistic is outside of the range of p-values available in the
look-up table. The actual p-value is greater than the p-value returned.

  kpss_result = kpss(series, regression='c')
C:\Users\loydt\AppData\Local\Temp\ipykernel_16620\4141645899.py:35: InterpolationWarning: The test statistic is outside of the range of p-values available in the
look-up table. The actual p-value is smaller than the p-value returned.

  kpss_result = kpss(series, regression='c')
C:\Users\loydt\AppData\Local\Temp\ipykernel_16620\4141645899.py:35: InterpolationWarning: The test statistic is outside of the range of p-values available in the
look-up table. The actual p-value is smaller than the p-value returned.

  kpss_result = kpss(series, regression='c')
C:\Users\loydt\AppData\Local\Temp\ipykernel_16620\4141645899.py:35: InterpolationWarning: The test statistic is outside of the range of p-values available in the
look-up table. The actual p-value is smaller than the p-value returned.

  kpss_result = kpss(series, regression='c')
C:\Users\loydt\AppData\Local\Temp\ipykernel_16620\4141645899.py:35: InterpolationWarning: The test statistic is outside of the range of p-values available in the
look-up table. The actual p-value is smaller than the p-value returned.

  kpss_result = kpss(series, regression='c')
C:\Users\loydt\AppData\Local\Temp\ipykernel_16620\4141645899.py:35: InterpolationWarning: The test statistic is outside of the range of p-values available in the
look-up table. The actual p-value is greater than the p-value returned.

  kpss_result = kpss(series, regression='c')
C:\Users\loydt\AppData\Local\Temp\ipykernel_16620\4141645899.py:35: InterpolationWarning: The test statistic is outside of the range of p-values available in the
look-up table. The actual p-value is greater than the p-value returned.

  kpss_result = kpss(series, regression='c')
C:\Users\loydt\AppData\Local\Temp\ipykernel_16620\4141645899.py:35: InterpolationWarning: The test statistic is outside of the range of p-values available in the
look-up table. The actual p-value is greater than the p-value returned.

  kpss_result = kpss(series, regression='c')
"""

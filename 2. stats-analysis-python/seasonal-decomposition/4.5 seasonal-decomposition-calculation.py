import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose

# Function to load and preprocess data
def load_and_preprocess_data(file_path):
    data = pd.read_excel(file_path)
    data['Order Date'] = pd.to_datetime(data['Order Date'], format='%d/%m/%Y', errors='coerce')
    data.set_index('Order Date', inplace=True)
    return data

# Function to calculate monthly sales and averages
def calculate_monthly_sales_and_avg(data, sub_category):
    sub_category_data = data[data['Sub-Category'] == sub_category]
    monthly_sales = sub_category_data['Sales'].resample('ME').sum()
    monthly_counts = sub_category_data['Sales'].resample('ME').count()
    monthly_average_sales = monthly_sales / monthly_counts
    return monthly_sales, monthly_average_sales

# Function to perform seasonal decomposition and return components
def perform_seasonal_decomposition(monthly_sales):
    decomposition = seasonal_decompose(monthly_sales, model='additive', period=12)
    return decomposition.trend, decomposition.seasonal, decomposition.resid

# Function to calculate expected sales
def calculate_expected_sales(trend, seasonal):
    return trend - np.abs(seasonal)

# Function to calculate performance deviation
def calculate_performance_deviation(residual, expected_sales):
    return (residual / expected_sales) * 100

# Function to create results DataFrame for a sub-category
def create_sub_category_results(sub_category, monthly_sales, monthly_average_sales, trend, seasonal, residual, expected_sales, performance_deviation):
    sub_category_monthly_results = pd.DataFrame({
        'Order Date': monthly_sales.index,
        'Total Sales': monthly_sales,
        'Average Monthly Sales': monthly_average_sales,
        'Trend': trend,
        'Seasonal': seasonal,
        'Residual': residual,
        'Expected Sales': expected_sales,
        'Performance Deviation (%)': performance_deviation
    })
    sub_category_monthly_results['Sub-Category'] = sub_category
    return sub_category_monthly_results

# Function to filter valid results with non-null residual values
def filter_valid_results(results):
    return results[results['Residual'].notna()]

# Function to process all sub-categories and accumulate results
def process_sub_categories(data, sub_categories):
    monthly_results = pd.DataFrame()

    for sub_category in sub_categories:
        monthly_sales, monthly_average_sales = calculate_monthly_sales_and_avg(data, sub_category)
        trend, seasonal, residual = perform_seasonal_decomposition(monthly_sales)
        expected_sales = calculate_expected_sales(trend, seasonal)
        performance_deviation = calculate_performance_deviation(residual, expected_sales)
        
        sub_category_results = create_sub_category_results(
            sub_category, monthly_sales, monthly_average_sales, trend, seasonal, residual, expected_sales, performance_deviation
        )

        valid_results = filter_valid_results(sub_category_results)
        monthly_results = pd.concat([monthly_results, valid_results], ignore_index=True)

    return monthly_results

# Main function to run the entire process
def main():
    file_path = 'C:\\Users\\loydt\\Downloads\\Projects\\Superstore Sales Dataset.xlsx'
    data = load_and_preprocess_data(file_path)
    sub_categories = ['Bookcases', 'Chairs', 'Labels', 'Tables', 'Storage', 'Furnishings', 
                      'Art', 'Phones', 'Binders', 'Appliances', 'Paper', 'Accessories', 
                      'Envelopes', 'Fasteners', 'Supplies', 'Machines', 'Copiers']
    
    monthly_results = process_sub_categories(data, sub_categories)

    # Reset index for better readability and display the final results
    monthly_results.reset_index(drop=True, inplace=True)
    print(monthly_results)

# Run the main function
if __name__ == "__main__":
    main()


"""
Order Date  Total Sales  Average Monthly Sales        Trend     Seasonal  \
0   2015-07-31    1487.6730             743.836500  1702.839492  -117.200645   
1   2015-08-31     794.2760             397.138000  1747.785850  -698.696595   
2   2015-09-30    2394.4698             478.893960  1781.928783  4140.995774   
3   2015-10-31     616.9980             616.998000  1827.875508 -1075.097784   
4   2015-11-30    7263.7137             807.079300  1904.683738  4388.031677   
..         ...          ...                    ...          ...          ...   
600 2018-02-28       0.0000                    NaN  5077.442083 -3174.058897   
601 2018-03-31   21319.8220            3553.303667  5031.611167  5384.325020   
602 2018-04-30       0.0000                    NaN  4449.119167 -1959.512175   
603 2018-05-31    3359.9520            3359.952000  4426.622000  1581.033492   
604 2018-06-30       0.0000                    NaN  5066.618000 -3492.539008   

         Residual  Expected Sales  Performance Deviation (%) Sub-Category  
0      -97.965846     1585.638846                  -6.178320    Bookcases  
1     -254.813255     1049.089255                 -24.288997    Bookcases  
2    -3528.454757    -2359.066991                 149.569926    Bookcases  
3     -135.779724      752.777724                 -18.037160    Bookcases  
4      970.998286    -2483.347939                 -39.100372    Bookcases  
..            ...             ...                        ...          ...  
600  -1903.383186     1903.383186                -100.000000      Copiers  
601  10903.885814     -352.713853               -3091.425449      Copiers  
602  -2489.606992     2489.606992                -100.000000      Copiers  
603  -2647.703492     2845.588508                 -93.045902      Copiers  
604  -1574.078992     1574.078992                -100.000000      Copiers  

[605 rows x 9 columns]
"""

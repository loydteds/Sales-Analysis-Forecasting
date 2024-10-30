import pandas as pd
import statsmodels.api as sm
import plotly.graph_objs as go
import os

# Load the dataset
file_path = 'C:\\Users\\loydt\\Downloads\\Projects\\Superstore Sales Dataset.xlsx'
data = pd.read_excel(file_path)

# Convert the 'Order Date' column to datetime
data['Order Date'] = pd.to_datetime(data['Order Date'], format='%d/%m/%Y', errors='coerce')

# Set 'Order Date' as the index
data.set_index('Order Date', inplace=True)

# List of unique sub-categories
sub_categories = ['Bookcases', 'Chairs', 'Labels', 'Tables', 'Storage', 'Furnishings', 
                  'Art', 'Phones', 'Binders', 'Appliances', 'Paper', 'Accessories', 
                  'Envelopes', 'Fasteners', 'Supplies', 'Machines', 'Copiers']

# Create a directory for saving results
output_dir = 'Sales_Performance_Results'
os.makedirs(output_dir, exist_ok=True)

# Loop through each sub-category to create individual charts and save results
for sub_category in sub_categories:
    # Filter data for the current sub-category
    sub_category_data = data[data['Sub-Category'] == sub_category]
    
    # Resample the data to get monthly sales
    monthly_sales = sub_category_data['Sales'].resample('ME').sum()
    
    # Perform seasonal decomposition
    decomposition = sm.tsa.seasonal_decompose(monthly_sales, model='additive', period=12)
    
    # Extract the seasonal and residual components
    seasonal = decomposition.seasonal
    residual = decomposition.resid
    
    # Initialize lists and totals
    expected_increases = []
    expected_drops = []
    expected_increases_exceeded = []
    below_expected_drops = []
    total_failed_expectations = 0
    total_exceeded_expectations = 0
    total_below_expected_drops = 0
    total_drop_exceeded_expectations = 0
    
    # Collect dates and values for expected increases and drops
    recorded_values = {date.date(): residual_value for date, residual_value in zip(residual.index, residual) if pd.notna(residual_value)}
    for date, seasonal_value in zip(seasonal.index, seasonal):
        if pd.notna(seasonal_value):
            if seasonal_value > 0:
                expected_increases.append((date.date(), seasonal_value))
            elif seasonal_value < 0:
                expected_drops.append((date.date(), seasonal_value))
    
    # Calculate performance metrics and record values
    results = []
    for date, expected_value in expected_increases:
        recorded_value = recorded_values.get(date)
        if recorded_value is not None:
            if expected_value > 0 and recorded_value < expected_value:
                failed_expectations = abs(expected_value - recorded_value)
                total_failed_expectations += failed_expectations
                results.append([date, "Expected Increase", expected_value, recorded_value, "Failed", failed_expectations])
            elif expected_value > 0 and recorded_value > expected_value:
                exceeded_expectations = abs(recorded_value - expected_value)
                total_exceeded_expectations += exceeded_expectations
                results.append([date, "Expected Increase", expected_value, recorded_value, "Exceeded", exceeded_expectations])

    for date, expected_value in expected_drops:
        recorded_value = recorded_values.get(date)
        if recorded_value is not None:
            if recorded_value < expected_value:
                failed_expectations = abs(expected_value - recorded_value)
                total_below_expected_drops += failed_expectations
                results.append([date, "Expected Drop", expected_value, recorded_value, "Below Expected", failed_expectations])
            elif recorded_value > expected_value:
                exceeded_expectations = abs(recorded_value - expected_value)
                total_drop_exceeded_expectations += exceeded_expectations
                results.append([date, "Expected Drop", expected_value, recorded_value, "Exceeded", exceeded_expectations])
    
    # Append total results
    results.append(["Total", "N/A", "N/A", "N/A", "Expected Increase but Failed Total", total_failed_expectations])
    results.append(["Total", "N/A", "N/A", "N/A", "Expected Increase and Exceeded Total", total_exceeded_expectations])
    results.append(["Total", "N/A", "N/A", "N/A", "Below Expected Drop Total", total_below_expected_drops])
    results.append(["Total", "N/A", "N/A", "N/A", "Expected Drop but Exceeded Total", total_drop_exceeded_expectations])

    # Save the results to a CSV file
    results_df = pd.DataFrame(results, columns=["Date", "Expectation Type", "Expected Value", "Recorded Value", "Status", "Value Difference"])
    results_df.to_csv(os.path.join(output_dir, f"{sub_category}_Sales_Performance.csv"), index=False)    

print("Performance evaluation files saved for each sub-category.")

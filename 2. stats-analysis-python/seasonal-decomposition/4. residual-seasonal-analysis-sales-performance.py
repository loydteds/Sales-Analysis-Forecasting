import pandas as pd
import statsmodels.api as sm
import plotly.graph_objs as go

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

# Loop through each sub-category to create individual charts
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
    
    # Print the dates with corresponding seasonal values for performance evaluation
    print(f"\nSales Performance Evaluation for {sub_category}:")
    
    # Initialize lists to collect expected increases, drops, exceeded expectations, and below expected drops
    expected_increases = []
    expected_drops = []
    expected_increases_exceeded = []
    below_expected_drops = []

    # Initialize totals for each category
    total_failed_expectations = 0
    total_exceeded_expectations = 0
    total_below_expected_drops = 0
    total_drop_exceeded_expectations = 0
    
    for date, seasonal_value, residual_value in zip(seasonal.index, seasonal, residual):
        if pd.notna(residual_value):  # Check if the residual value is not NaN
            if seasonal_value < 0:
                # Collect negative seasonal values
                expected_drops.append((date.date(), seasonal_value))
            elif seasonal_value > 0:
                # Collect positive seasonal values
                expected_increases.append((date.date(), seasonal_value))

    # Prepare recorded values for residuals
    recorded_values = {}
    
    for date, residual_value in zip(residual.index, residual):
        if pd.notna(residual_value):  # Check if the residual value is not NaN
            recorded_values[date.date()] = residual_value

    # Print expected increases and corresponding recorded values
    print("\nFor Expected Increase but Failed:")
    print("Date | Expected Increase | Recorded Value | Failed Expectations")
    
    for date, expected_value in expected_increases:
        recorded_value = recorded_values.get(date)
        if recorded_value is not None:
            if expected_value > 0 and recorded_value < expected_value:
                failed_expectations = abs(expected_value - recorded_value)
                total_failed_expectations += failed_expectations
                print(f"{date} | {expected_value:.2f} | {recorded_value:.2f} | {failed_expectations:.2f}")
            elif expected_value > 0 and recorded_value > expected_value:
                exceeded_expectations = abs(recorded_value - expected_value)
                total_exceeded_expectations += exceeded_expectations
                expected_increases_exceeded.append((date, expected_value, recorded_value, exceeded_expectations))

    # Print expected increases and exceeded expectations
    print("\nFor Expected Increase and Exceeded:")
    print("Date | Expected Increase | Recorded Value | Exceeded Expectations")

    for date, expected_value, recorded_value, exceeded_expectations in expected_increases_exceeded:
        print(f"{date} | {expected_value:.2f} | {recorded_value:.2f} | {exceeded_expectations:.2f}")

    # Print expected drops and corresponding recorded values for Below Expected Drop list
    print("\nBelow Expected Drop:")
    print("Date | Expected Drop | Recorded Value | Failed Expectations")
    
    for date, expected_value in expected_drops:
        recorded_value = recorded_values.get(date)
        if recorded_value is not None:
            if recorded_value < expected_value:
                failed_expectations = abs(expected_value - recorded_value)
                total_below_expected_drops += failed_expectations
                below_expected_drops.append((date, expected_value, recorded_value, failed_expectations))
                print(f"{date} | {expected_value:.2f} | {recorded_value:.2f} | {failed_expectations:.2f}")

    # Print expected drops and corresponding recorded values
    print("\nFor Expected Drop but Exceeded:")
    print("Date | Expected Drop | Recorded Value | Exceeded Expectations")

    for date, expected_value in expected_drops:
        recorded_value = recorded_values.get(date)
        if recorded_value is not None:
            exceeded_expectations = abs(max(expected_value, recorded_value) - min(expected_value, recorded_value))
            total_drop_exceeded_expectations += exceeded_expectations
            print(f"{date} | {expected_value:.2f} | {recorded_value:.2f} | {exceeded_expectations:.2f}")

    # Print total values for each category
    print(f"\nTotal for {sub_category}:")
    print(f"Expected Increase but Failed Total: {total_failed_expectations:.2f}")
    print(f"Expected Increase and Exceeded Total: {total_exceeded_expectations:.2f}")
    print(f"Below Expected Drop Total: {total_below_expected_drops:.2f}")
    print(f"Expected Drop but Exceeded Total: {total_drop_exceeded_expectations:.2f}")

    # Create a line plot for seasonal and residual components
    fig = go.Figure()

    # Add seasonal component
    fig.add_trace(go.Scatter(
        x=seasonal.index,
        y=seasonal,
        mode='lines',
        name='Seasonal Component',
        line=dict(width=2)
    ))

    # Add residual component with custom color and line style
    fig.add_trace(go.Scatter(
        x=residual.index,
        y=residual,
        mode='lines',
        name='Residual Component',
        line=dict(width=2, dash='dash', color='orange')
    ))

    # Update layout with dark theme
    fig.update_layout(
        title=f'Seasonal and Residual Components for {sub_category}',
        xaxis_title='Date',
        yaxis_title='Value',
        legend_title='Components',
        template='plotly_dark'
    )

    # Show the figure
    fig.show()

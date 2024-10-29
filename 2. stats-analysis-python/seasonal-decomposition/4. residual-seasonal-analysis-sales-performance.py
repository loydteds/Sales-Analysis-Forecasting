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
    
    # Print the dates with corresponding seasonal and residual values for performance evaluation
    print(f"\nSales Performance Evaluation for {sub_category}:")
    for date, seasonal_value, residual_value in zip(seasonal.index, seasonal, residual):
        if pd.notna(residual_value):
            # Check conditions for evaluation
            if seasonal_value < 0:  # Condition for negative seasonal value
                if residual_value == seasonal_value:
                    status = "Sales Meets Expectations"
                elif residual_value > seasonal_value:
                    status = "Sales Exceeds Expectations"
                else:
                    status = "Sales Fails to Meet Expectations"
            else:  # Condition for positive seasonal value
                if residual_value == seasonal_value:
                    status = "Sales Meets Expectations"
                elif residual_value > seasonal_value:
                    status = "Sales Exceeds Expectations"
                else:
                    status = "Sales Fails to Meet Expectations"
            
            print(f"Date: {date.date()}, Seasonal Value: {seasonal_value:.2f}, "
                  f"Residual Value: {residual_value:.2f} - {status}")

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
        template='plotly_dark'  # Apply dark theme
    )

    # Show the figure
    fig.show()

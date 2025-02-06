import pandas as pd
import statsmodels.api as sm
import plotly.graph_objs as go

# Function to load the dataset
def load_data(file_path: str):
    data = pd.read_excel(file_path)
    data['Order Date'] = pd.to_datetime(data['Order Date'], format='%d/%m/%Y', errors='coerce')
    data.set_index('Order Date', inplace=True)
    return data

# Function to get the list of unique sub-categories
def get_sub_categories():
    return [
        'Bookcases', 'Chairs', 'Labels', 'Tables', 'Storage', 'Furnishings', 
        'Art', 'Phones', 'Binders', 'Appliances', 'Paper', 'Accessories', 
        'Envelopes', 'Fasteners', 'Supplies', 'Machines', 'Copiers'
    ]

# Function to filter data by sub-category and resample to get monthly sales
def get_monthly_sales(data, sub_category: str):
    sub_category_data = data[data['Sub-Category'] == sub_category]
    return sub_category_data['Sales'].resample('ME').sum()

# Function to perform seasonal decomposition
def perform_seasonal_decomposition(monthly_sales):
    return sm.tsa.seasonal_decompose(monthly_sales, model='additive', period=12)

# Function to plot the residual component using Plotly
def plot_residual_component(residual, sub_category: str):
    fig = go.Figure()

    # Residual plot (lines with dots)
    fig.add_trace(go.Scatter(x=residual.index, y=residual, mode='lines+markers', name='Residual', 
                             line=dict(color='orange'), marker=dict(color='orange', size=6)))
    
    # Update layout for aesthetics
    fig.update_layout(
        height=600, 
        width=1000, 
        title=f'Residual Component of {sub_category} Sales', 
        showlegend=False,
        paper_bgcolor='rgba(45, 45, 45, 1)',  # Background outside the plot area
        plot_bgcolor='rgba(40, 40, 40, 1)',   # Background inside the plot area
        xaxis=dict(showgrid=True, gridcolor='gray'),
        yaxis=dict(showgrid=True, gridcolor='gray'),
        title_font=dict(size=18, color='white'),
        xaxis_title='Date',
        yaxis_title='Sales',
        font=dict(color='white'),
        xaxis_title_font=dict(size=14),
        yaxis_title_font=dict(size=14),
    )
    
    # Show the figure
    fig.show()

# Main function to process the sales data
def process_sales_data(file_path: str):
    # Load the dataset
    data = load_data(file_path)

    # Get sub-categories
    sub_categories = get_sub_categories()

    # Loop through each sub-category
    for sub_category in sub_categories:
        # Get monthly sales data
        monthly_sales = get_monthly_sales(data, sub_category)
        
        # Skip sub-categories with no data
        if monthly_sales.empty:
            print(f"No data available for {sub_category}. Skipping...")
            continue
        
        # Perform seasonal decomposition
        decomposition = perform_seasonal_decomposition(monthly_sales)
        
        # Extract the residual component
        residual = decomposition.resid.dropna()  # Drop NaN values from residual component

        # Plot the residual component
        plot_residual_component(residual, sub_category)

# File path for the dataset
file_path = 'C:\\Users\\loydt\\Downloads\\Projects\\Superstore Sales Dataset.xlsx'

# Execute the main function
process_sales_data(file_path)

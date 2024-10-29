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

# Loop through each sub-category
for sub_category in sub_categories:
    # Filter data for the current sub-category
    sub_category_data = data[data['Sub-Category'] == sub_category]
    
    # Resample the data to get monthly sales
    monthly_sales = sub_category_data['Sales'].resample('ME').sum()
    
    # Perform seasonal decomposition
    decomposition = sm.tsa.seasonal_decompose(monthly_sales, model='additive', period=12)
    
    # Extract the seasonal component
    seasonal = decomposition.seasonal

     # Print the dates and their corresponding seasonal values
    print(f"\nSeasonal values for {sub_category}:")
    for date, value in seasonal.items():
        print(f"Date: {date.date()}, Seasonal Value: {value:.2f}")
    
    # Create a Plotly figure for the seasonal component
    fig = go.Figure()

    # Seasonal plot (lines with dots)
    fig.add_trace(go.Scatter(x=seasonal.index, y=seasonal, mode='lines+markers', name='Seasonal', 
                             line=dict(color='orange'), marker=dict(color='orange', size=6)))
    
    # Update layout for aesthetics
    fig.update_layout(
        height=600, 
        width=1000, 
        title=f'Seasonal Component of {sub_category} Sales', 
        showlegend=False,
        
        # Set the background color to a darker shade
        paper_bgcolor='rgba(45, 45, 45, 1)',  # Background outside the plot area
        plot_bgcolor='rgba(40, 40, 40, 1)',   # Background inside the plot area
        
        # Enable gridlines by setting showgrid to True
        xaxis=dict(showgrid=True, gridcolor='gray'),
        yaxis=dict(showgrid=True, gridcolor='gray'),
        
        # Customize the title and font color
        title_font=dict(size=18, color='white'),
        xaxis_title='Date',
        yaxis_title='Sales',
        font=dict(color='white'),
        
        # Font size for axis titles
        xaxis_title_font=dict(size=14),
        yaxis_title_font=dict(size=14),
    )
    
    # Show the figure
    fig.show()

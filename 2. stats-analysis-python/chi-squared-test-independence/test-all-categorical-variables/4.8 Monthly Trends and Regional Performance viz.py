import pandas as pd
import plotly.express as px
import plotly.io as pio

# Set Plotly to dark theme
pio.templates.default = "plotly_dark"

# Function to load the dataset
def load_data(file_path):
    """Load dataset from a specified file path."""
    return pd.read_excel(file_path)

# Function to preprocess data: Convert 'Order Date' to datetime and extract month, year, and create Year-Month column
def preprocess_data(data):
    """Convert 'Order Date' to datetime and extract month, year, and Year-Month column."""
    data['Order Date'] = pd.to_datetime(data['Order Date'])
    data['Order Month'] = data['Order Date'].dt.month
    data['Order Year'] = data['Order Date'].dt.year
    data['Order Year-Month'] = pd.to_datetime(dict(year=data['Order Year'], month=data['Order Month'], day=1))
    return data

# Function to create a line plot for monthly sales by segment or ship mode
def create_sales_line_plot(data, group_by_column, title, color_column):
    """Create a line plot for monthly sales based on a grouping column (Segment or Ship Mode)."""
    monthly_sales = data.groupby(['Order Year-Month', group_by_column])['Sales'].sum().reset_index()
    fig = px.line(
        monthly_sales,
        x='Order Year-Month',
        y='Sales',
        color=group_by_column,
        title=title,
        labels={"x": "Order Date", "Sales": "Total Sales"}
    )
    fig.update_layout(
        xaxis=dict(title='Order Date'),
        yaxis=dict(title='Sales'),
        legend_title_text=group_by_column
    )
    return fig

# Function to create a treemap for sales distribution by region, state, and category
def create_sales_treemap(data):
    """Create a treemap visualization for sales distribution by region, state, and category."""
    state_region_category_sales = data.groupby(['State', 'Region', 'Category'])['Sales'].sum().reset_index()
    fig = px.treemap(
        state_region_category_sales,
        path=['Region', 'State', 'Category'],
        values='Sales',
        color='Sales',
        title="Sales Distribution by Region, State, and Category",
        color_continuous_scale="Blues"
    )
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    return fig

# Main analysis workflow
def main(file_path):
    # Load and preprocess data
    data = load_data(file_path)
    data = preprocess_data(data)
    
    # Create and show sales trends by segment
    fig_segment = create_sales_line_plot(data, 'Segment', "Monthly Sales Trend by Segment", 'Segment')
    fig_segment.show()
    
    # Create and show sales trends by ship mode
    fig_ship_mode = create_sales_line_plot(data, 'Ship Mode', "Monthly Sales Trend by Ship Mode", 'Ship Mode')
    fig_ship_mode.show()
    
    # Create and show sales distribution by region, state, and category
    fig_region = create_sales_treemap(data)
    fig_region.show()

# Run the analysis
if __name__ == "__main__":
    file_path = 'C:\\Users\\loydt\\Downloads\\Projects\\Superstore Sales Dataset.xlsx'
    main(file_path)

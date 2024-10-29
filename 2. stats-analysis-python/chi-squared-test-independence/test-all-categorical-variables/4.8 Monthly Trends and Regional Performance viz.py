import pandas as pd
import plotly.express as px
import plotly.io as pio

# Set Plotly to dark theme
pio.templates.default = "plotly_dark"

# Load the dataset
file_path = 'C:\\Users\\loydt\\Downloads\\Projects\\Superstore Sales Dataset.xlsx'
data = pd.read_excel(file_path)

# Convert 'Order Date' to datetime and extract month and year
data['Order Date'] = pd.to_datetime(data['Order Date'])
data['Order Month'] = data['Order Date'].dt.month
data['Order Year'] = data['Order Date'].dt.year

# Combine 'Order Year' and 'Order Month' with a placeholder day=1
data['Order Year-Month'] = pd.to_datetime(dict(year=data['Order Year'], month=data['Order Month'], day=1))

# Time Series Visualization: Monthly Sales by Segment
monthly_sales_segment = data.groupby(['Order Year-Month', 'Segment'])['Sales'].sum().reset_index()
fig_segment = px.line(
    monthly_sales_segment,
    x='Order Year-Month',
    y='Sales',
    color='Segment',
    title="Monthly Sales Trend by Segment",
    labels={"x": "Order Date", "Sales": "Total Sales"}
)
fig_segment.update_layout(xaxis=dict(title='Order Date'), yaxis=dict(title='Sales'), legend_title_text='Segment')
fig_segment.show()

# Time Series Visualization: Monthly Sales by Ship Mode
monthly_sales_ship_mode = data.groupby(['Order Year-Month', 'Ship Mode'])['Sales'].sum().reset_index()
fig_ship_mode = px.line(
    monthly_sales_ship_mode,
    x='Order Year-Month',
    y='Sales',
    color='Ship Mode',
    title="Monthly Sales Trend by Ship Mode",
    labels={"x": "Order Date", "Sales": "Total Sales"}
)
fig_ship_mode.update_layout(xaxis=dict(title='Order Date'), yaxis=dict(title='Sales'), legend_title_text='Ship Mode')
fig_ship_mode.show()

# Regional Insights: State and Region Interactions for Product Categories
state_region_category_sales = data.groupby(['State', 'Region', 'Category'])['Sales'].sum().reset_index()
fig_region = px.treemap(
    state_region_category_sales,
    path=['Region', 'State', 'Category'],
    values='Sales',
    color='Sales',
    title="Sales Distribution by Region, State, and Category",
    color_continuous_scale="Blues"
)
fig_region.update_layout(margin=dict(t=50, l=25, r=25, b=25))
fig_region.show()

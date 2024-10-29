import pandas as pd
import plotly.express as px

# Load the dataset
file_path = 'C:\\Users\\loydt\\Downloads\\Projects\\Superstore Sales Dataset.xlsx'
data = pd.read_excel(file_path)

# Convert 'Order Date' to datetime format if it's not already
data['Order Date'] = pd.to_datetime(data['Order Date'])

# Extract the month from the 'Order Date'
data['Order Month'] = data['Order Date'].dt.month

# Count the frequency of transactions per city
city_counts = data['City'].value_counts().reset_index()
city_counts.columns = ['City', 'Transaction Count']

# Sort the cities from highest to lowest based on transaction count
city_counts = city_counts.sort_values(by='Transaction Count', ascending=False)

# Create the bar chart
fig = px.bar(city_counts, 
              x='City', 
              y='Transaction Count', 
              title='Transaction Frequency by City',
              color='Transaction Count', 
              color_continuous_scale=px.colors.sequential.Darkmint)  # Using a dark color scale
              
# Update layout for better appearance
fig.update_layout(
    xaxis_title='City',
    yaxis_title='Transaction Count',
    xaxis_tickangle=-45,
    template='plotly_dark'  # Use a dark template
)

# Show the plot
fig.show()

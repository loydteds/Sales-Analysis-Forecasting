import pandas as pd
import plotly.express as px

# Function to load the dataset
def load_data(file_path):
    """Load dataset from a specified file path."""
    return pd.read_excel(file_path)

# Function to preprocess data by converting 'Order Date' to datetime and extracting the month
def preprocess_data(data):
    """Convert 'Order Date' to datetime and extract the month."""
    data['Order Date'] = pd.to_datetime(data['Order Date'])
    data['Order Month'] = data['Order Date'].dt.month
    return data

# Function to count transactions per city
def count_transactions_by_city(data):
    """Count the frequency of transactions per city."""
    city_counts = data['City'].value_counts().reset_index()
    city_counts.columns = ['City', 'Transaction Count']
    city_counts = city_counts.sort_values(by='Transaction Count', ascending=False)
    return city_counts

# Function to create and return a bar chart figure
def create_bar_chart(city_counts):
    """Create a bar chart for transaction frequency by city."""
    fig = px.bar(city_counts, 
                 x='City', 
                 y='Transaction Count', 
                 title='Transaction Frequency by City',
                 color='Transaction Count', 
                 color_continuous_scale=px.colors.sequential.Darkmint)  # Dark color scale
                 
    # Update layout for better appearance
    fig.update_layout(
        xaxis_title='City',
        yaxis_title='Transaction Count',
        xaxis_tickangle=-45,
        template='plotly_dark'  # Dark template
    )
    return fig

# Function to display the plot
def display_plot(fig):
    """Display the plot."""
    fig.show()

# Main analysis workflow
def main(file_path):
    # Load the data
    data = load_data(file_path)
    
    # Preprocess the data (convert 'Order Date' and extract the month)
    data = preprocess_data(data)
    
    # Count transactions per city
    city_counts = count_transactions_by_city(data)
    
    # Create the bar chart
    fig = create_bar_chart(city_counts)
    
    # Display the plot
    display_plot(fig)

# Run the analysis
if __name__ == "__main__":
    file_path = 'C:\\Users\\loydt\\Downloads\\Projects\\Superstore Sales Dataset.xlsx'
    main(file_path)

import pandas as pd
import statsmodels.api as sm
import plotly.graph_objs as go

# Utility function to load data
def load_data(file_path):
    """Load data from an Excel file."""
    return pd.read_excel(file_path)

# Function to prepare data for analysis
def preprocess_data(data):
    """Preprocess the data: convert 'Order Date' to datetime and set it as the index."""
    data['Order Date'] = pd.to_datetime(data['Order Date'], format='%d/%m/%Y', errors='coerce')
    data.set_index('Order Date', inplace=True)
    return data

# Function to perform seasonal decomposition
def seasonal_decomposition(monthly_sales):
    """Perform seasonal decomposition on the sales data."""
    return sm.tsa.seasonal_decompose(monthly_sales, model='additive', period=12)

# Function to collect seasonal and residual data
def extract_seasonal_residual(decomposition):
    """Extract seasonal and residual components from the decomposition."""
    return decomposition.seasonal, decomposition.resid

# Function to analyze expected increases and drops
def analyze_performance(seasonal, residual):
    """Analyze expected increases and drops based on seasonal and residual data."""
    expected_increases, expected_drops, expected_increases_exceeded, below_expected_drops = [], [], [], []
    recorded_values = {date.date(): value for date, value in zip(residual.index, residual) if pd.notna(value)}
    
    for date, seasonal_value in zip(seasonal.index, seasonal):
        if pd.notna(seasonal_value):
            if seasonal_value < 0:
                expected_drops.append((date.date(), seasonal_value))
            elif seasonal_value > 0:
                expected_increases.append((date.date(), seasonal_value))
    
    for date, expected_value in expected_increases:
        recorded_value = recorded_values.get(date)
        if recorded_value and recorded_value < expected_value:
            expected_increases_exceeded.append((date, expected_value, recorded_value, abs(expected_value - recorded_value)))
    
    for date, expected_value in expected_drops:
        recorded_value = recorded_values.get(date)
        if recorded_value and recorded_value < expected_value:
            below_expected_drops.append((date, expected_value, recorded_value, abs(expected_value - recorded_value)))
    
    return expected_increases, expected_drops, expected_increases_exceeded, below_expected_drops, recorded_values

# Function to print evaluation results
def print_evaluation(sub_category, expected_increases, expected_drops, expected_increases_exceeded, below_expected_drops):
    """Print the sales performance evaluation results."""
    print(f"\nSales Performance Evaluation for {sub_category}:")
    
    def print_category(title, data, headers):
        print(f"\n{title}:")
        print(" | ".join(headers))
        for entry in data:
            print(f"{entry[0]} | {entry[1]:.2f} | {entry[2]:.2f} | {entry[3]:.2f}")
    
    # Print results for each category
    print_category("For Expected Increase but Failed", expected_increases, ["Date", "Expected Increase", "Recorded Value", "Failed Expectations"])
    print_category("For Expected Increase and Exceeded", expected_increases_exceeded, ["Date", "Expected Increase", "Recorded Value", "Exceeded Expectations"])
    print_category("For Below Expected Drop", below_expected_drops, ["Date", "Expected Drop", "Recorded Value", "Failed Expectations"])

# Function to create the plot
def create_plot(sub_category, seasonal, residual):
    """Create and display a plot for the seasonal and residual components."""
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

# Main function to process sub-categories
def process_sub_category(data, sub_category):
    """Process the data for a specific sub-category."""
    sub_category_data = data[data['Sub-Category'] == sub_category]
    monthly_sales = sub_category_data['Sales'].resample('ME').sum()

    # Perform seasonal decomposition
    decomposition = seasonal_decomposition(monthly_sales)

    # Extract seasonal and residual components
    seasonal, residual = extract_seasonal_residual(decomposition)

    # Analyze performance
    expected_increases, expected_drops, expected_increases_exceeded, below_expected_drops, recorded_values = analyze_performance(seasonal, residual)

    # Print evaluation results
    print_evaluation(sub_category, expected_increases, expected_drops, expected_increases_exceeded, below_expected_drops)

    # Create and display the plot
    create_plot(sub_category, seasonal, residual)

# Main execution function
def main(file_path):
    """Main function to execute the analysis for each sub-category."""
    # Load and preprocess data
    data = load_data(file_path)
    data = preprocess_data(data)

    # List of unique sub-categories
    sub_categories = ['Bookcases', 'Chairs', 'Labels', 'Tables', 'Storage', 'Furnishings', 
                      'Art', 'Phones', 'Binders', 'Appliances', 'Paper', 'Accessories', 
                      'Envelopes', 'Fasteners', 'Supplies', 'Machines', 'Copiers']

    # Process each sub-category
    for sub_category in sub_categories:
        process_sub_category(data, sub_category)

# Run the main function with the file path
if __name__ == "__main__":
    file_path = 'C:\\Users\\loydt\\Downloads\\Projects\\Superstore Sales Dataset.xlsx'
    main(file_path)

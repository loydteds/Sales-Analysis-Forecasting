import pandas as pd

# Function to load the dataset
def load_data(file_path):
    """Load dataset from the given file path."""
    return pd.read_excel(file_path)

# Function to group and sum sales by Region, State, and Category
def group_sales_by_region_state_category(data):
    """Group data by Region, State, and Category and calculate total sales."""
    return data.groupby(['Region', 'State', 'Category'])['Sales'].sum().reset_index()

# Function to sort the sales distribution data
def sort_sales_data(sales_data):
    """Sort the sales data by Region, State, and Sales in descending order."""
    return sales_data.sort_values(by=['Region', 'State', 'Sales'], ascending=[True, True, False])

# Main workflow function
def main(file_path):
    # Load data
    data = load_data(file_path)
    
    # Group data by Region, State, and Category
    sales_distribution = group_sales_by_region_state_category(data)
    
    # Sort the sales distribution data for better readability
    sorted_sales_distribution = sort_sales_data(sales_distribution)
    
    # Print the resulting sorted sales distribution
    print("Sales Distribution by Region, State, and Category:")
    print(sorted_sales_distribution)

# Run the analysis
if __name__ == "__main__":
    file_path = 'C:\\Users\\loydt\\Downloads\\Projects\\Superstore Sales Dataset.xlsx'
    main(file_path)


"""
Sales Distribution by Region, State, and Category:
      Region       State         Category      Sales
2    Central    Illinois       Technology  31637.881
0    Central    Illinois        Furniture  28212.978
1    Central    Illinois  Office Supplies  19385.658
5    Central     Indiana       Technology  25959.670
4    Central     Indiana  Office Supplies  13206.860
..       ...         ...              ...        ...
137     West        Utah       Technology   2309.904
140     West  Washington       Technology  50536.710
138     West  Washington        Furniture  44626.472
139     West  Washington  Office Supplies  40043.668
141     West     Wyoming        Furniture   1603.136

[142 rows x 4 columns]
"""

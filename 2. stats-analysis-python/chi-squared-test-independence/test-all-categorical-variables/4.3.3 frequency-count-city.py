import pandas as pd

# Function to load data
def load_data(file_path):
    """Load dataset from a specified file path."""
    return pd.read_excel(file_path)

# Function to count total transaction frequency per city
def count_city_sales(data):
    """Count the total transaction frequency per city."""
    return data.groupby('City').size().reset_index(name='Total Sales Frequency')

# Function to count segment-specific transactions per city
def count_segment_sales(data):
    """Count segment-specific transaction frequency for each city."""
    segment_counts = data.groupby(['City', 'Segment']).size().unstack(fill_value=0).reset_index()
    segment_counts.columns.name = None  # Remove the name from the columns index
    return segment_counts

# Function to merge city sales with segment counts
def merge_sales_data(city_sales_counts, segment_counts):
    """Merge total city sales with segment-specific sales counts."""
    return pd.merge(city_sales_counts, segment_counts, on='City')

# Function to display results
def display_results(city_segment_counts):
    """Display the final merged sales data."""
    print("City-wise Sales Frequency with Segment Breakdown:")
    print(city_segment_counts)

# Main analysis workflow
def main(file_path):
    # Load the data
    data = load_data(file_path)
    
    # Count total sales and segment-specific sales
    city_sales_counts = count_city_sales(data)
    segment_counts = count_segment_sales(data)
    
    # Merge the sales data
    city_segment_counts = merge_sales_data(city_sales_counts, segment_counts)
    
    # Display the results
    display_results(city_segment_counts)

# Run the analysis
if __name__ == "__main__":
    file_path = 'C:\\Users\\loydt\\Downloads\\Projects\\Superstore Sales Dataset.xlsx'
    main(file_path)


"""
City-wise Sales Frequency with Segment Breakdown:
            City  Total Sales Frequency  Consumer  Corporate  Home Office
0       Aberdeen                      1         1          0            0
1        Abilene                      1         1          0            0
2          Akron                     20        13          6            1
3    Albuquerque                     14         4          4            6
4     Alexandria                     16         3          6            7
..           ...                    ...       ...        ...          ...
524   Woonsocket                      4         1          3            0
525      Yonkers                     15        13          0            2
526         York                      5         0          5            0
527      Yucaipa                      1         0          1            0
528         Yuma                      4         0          2            2

[529 rows x 5 columns]
"""

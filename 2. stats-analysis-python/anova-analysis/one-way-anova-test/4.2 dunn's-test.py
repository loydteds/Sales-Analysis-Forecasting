import pandas as pd
import math
import plotly.express as px
from scipy.stats import levene, bartlett, f_oneway
import scikit_posthocs as sp

# Load the dataset
file_path = 'C:\\Users\\loydt\\Downloads\\Projects\\Superstore Sales Dataset.xlsx'
data = pd.read_excel(file_path)

# Filter the big four states generating higher sales
states_of_interest = ['Washington', 'California', 'New York', 'Florida', 'Pennsylvania']
state_data = data[data['State'].isin(states_of_interest)]

# Extract relevant columns and create a deep copy to avoid SettingWithCopyWarning
high_sales_states = state_data[['Segment', 'State', 'City', 'Region', 'Ship Mode', 'Order Date', 'Category', 'Sub-Category', 'Product Name', 'Sales']].copy()

# Take logarithm of the Sales column, ensuring non-positive values are handled
high_sales_states['log_sales'] = high_sales_states['Sales'].apply(lambda x: math.log(x) if x > 0 else None)

# Check for null values in 'log_sales' after transformation
if high_sales_states['log_sales'].isnull().any():
    print("Warning: There are non-positive sales values that have been transformed to NaN.")

# Assuming `high_sales_states` is your DataFrame and you have filtered by the 'Category' variable
# Create a DataFrame with 'log_sales' and 'Category'
dunn_data = high_sales_states[['log_sales', 'Category']].dropna()  # Drop NaN values for valid analysis

# Conduct Dunn's Test
dunn_results = sp.posthoc_dunn(dunn_data, val_col='log_sales', group_col='Category', p_adjust='bonferroni')

# Display the results
print(dunn_results)

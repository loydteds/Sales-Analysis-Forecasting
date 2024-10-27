import pandas as pd
import math
import plotly.express as px
from scipy.stats import levene, bartlett, f_oneway
from statsmodels.formula.api import ols

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

# Create boxplot for log-transformed sales by each specified column
columns_to_plot = ['Sub-Category', 'State', 'Segment', 'Ship Mode', 'Region']

for column in columns_to_plot:
    boxplot_fig = px.box(
        high_sales_states,
        x=column,
        y="log_sales",
        title=f"Log-Transformed Sales by {column}",
        labels={column: column, "log_sales": "Log of Sales"},
        template="plotly_dark"
    )
    boxplot_fig.show()

# Loop through specified columns to perform Levene's and Bartlett's tests
columns_to_test = ['Sub-Category', 'State', 'Segment', 'Ship Mode', 'Region']

for column in columns_to_test:
    # Group the log-transformed sales data by the current column
    groups = [high_sales_states.loc[high_sales_states[column] == value, 'log_sales'].dropna() for value in high_sales_states[column].unique()]

    # Levene's Test
    levene_stat, levene_p = levene(*groups)
    print(f"Levene's Test Results for {column}:")
    print(f"Statistic: {levene_stat}, P-value: {levene_p}")
    if levene_p < 0.05:
        print("The variances across segments are significantly different (p < 0.05), indicating the assumption of homogeneity of variances is violated.\n")
    else:
        print("The variances across segments are not significantly different (p >= 0.05), indicating the assumption of homogeneity of variances is met.\n")

    # Bartlett's Test
    bartlett_stat, bartlett_p = bartlett(*groups)
    print(f"Bartlett's Test Results for {column}:")
    print(f"Statistic: {bartlett_stat}, P-value: {bartlett_p}")
    if bartlett_p < 0.05:
        print("The variances across segments are significantly different (p < 0.05), indicating the assumption of homogeneity of variances is violated.\n")
    else:
        print("The variances across segments are not significantly different (p >= 0.05), indicating the assumption of homogeneity of variances is met.\n")

# Check for missing values and ensure proper data types
print("Checking for missing values in the DataFrame:")
print(high_sales_states.isnull().sum())

# Perform ANOVA test for each specified categorical variable
for column in columns_to_test:  # type: ignore
    # Group the log-transformed sales data by the current column for ANOVA test
    groups = [high_sales_states.loc[high_sales_states[column] == group, 'log_sales'].dropna() 
              for group in high_sales_states[column].unique()]

    # Perform ANOVA test
    anova_result = f_oneway(*groups)
    print(f"\nANOVA Test Results for {column}:")
    print(f"F-statistic: {anova_result.statistic}")
    print(f"P-value: {anova_result.pvalue}")

    # Interpretation
    if anova_result.pvalue < 0.05:
        print("Reject the null hypothesis: Significant differences between groups.")
    else:
        print("Fail to reject the null hypothesis: No significant differences between groups.")

    # Print separator for clarity
    print("\n" + "="*80 + "\n")

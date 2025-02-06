import pandas as pd
import scipy.stats as stats
import itertools
from statsmodels.stats.multitest import multipletests

# Load the dataset
def load_data(file_path):
    """Load the dataset from a specified file path."""
    return pd.read_excel(file_path)

# Convert 'Order Date' to datetime format and extract the month
def preprocess_data(data):
    """Preprocess data by converting 'Order Date' to datetime and extracting the 'Order Month'."""
    data['Order Date'] = pd.to_datetime(data['Order Date'])
    data['Order Month'] = data['Order Date'].dt.month
    return data

# Conduct Chi-squared test and return results
def chi_squared_test(data, variable1, variable2, smoothing=0.5):
    """Conduct a Chi-squared test on two categorical variables."""
    contingency_table = pd.crosstab(data[variable1], data[variable2])
    contingency_table += smoothing  # Add smoothing to avoid zeros
    chi2, p, dof, _ = stats.chi2_contingency(contingency_table)
    return chi2, p, dof, contingency_table

# Filter significant results based on p-value threshold
def filter_significant_results(results, threshold=0.05):
    """Filter results that are statistically significant."""
    return [result for result in results if result[2] < threshold]

# Conduct post-hoc pairwise comparisons
def posthoc_comparisons(table):
    """Perform post-hoc pairwise comparisons for significant Chi-squared results."""
    pairs = list(itertools.combinations(table.index, 2))
    p_values = []
    
    for pair in pairs:
        sub_table = table.loc[list(pair)]
        try:
            _, p_pair, _, _ = stats.chi2_contingency(sub_table)
            p_values.append(p_pair)
        except ValueError:
            p_values.append(1)  # If error occurs, assign non-significant p-value
    
    # Adjust p-values using the Bonferroni correction
    corrected_p_values = multipletests(p_values, method='bonferroni')[1]
    return dict(zip(pairs, corrected_p_values))

# Display results
def display_results(posthoc_results):
    """Display the post-hoc results with corrected p-values."""
    for variable, results in posthoc_results.items():
        print(f"\nPost-hoc results for {variable} with Segment:")
        for pair, p_val in results.items():
            print(f"{pair}: Adjusted p-value = {p_val}")

# Main analysis workflow
def main(file_path):
    # Load and preprocess data
    data = load_data(file_path)
    data = preprocess_data(data)
    
    # Variables to test
    variables_to_test = ['State', 'City', 'Ship Mode', 'Order Month']
    significant_results = []
    
    # Conduct Chi-squared tests for each variable
    for variable in variables_to_test:
        try:
            chi2, p, dof, table = chi_squared_test(data, 'Segment', variable)
            significant_results.append((variable, chi2, p, dof, table))
            print(f"{variable}: Chi-squared = {chi2}, p = {p}, DoF = {dof}")
        except ValueError as e:
            print(f"Skipping {variable} due to error: {e}")
    
    # Filter significant results
    significant_results = filter_significant_results(significant_results)
    
    # Post-hoc analysis
    posthoc_results = {}
    for variable, chi2, p, dof, table in significant_results:
        posthoc_results[variable] = posthoc_comparisons(table)
    
    # Display results
    display_results(posthoc_results)

# Run the analysis
if __name__ == "__main__":
    file_path = 'C:\\Users\\loydt\\Downloads\\Projects\\Superstore Sales Dataset.xlsx'
    main(file_path)

"""
State: Chi-squared = 249.36663742175628, p = 1.3908748204941375e-15, DoF = 96
City: Chi-squared = 2015.006789463118, p = 1.5748980369915456e-62, DoF = 1056
Ship Mode: Chi-squared = 25.763379077286622, p = 0.0002464086024327002, DoF = 6
Order Month: Chi-squared = 63.66829835544393, p = 6.302173847865037e-06, DoF = 22

Post-hoc results for State with Segment:
('Consumer', 'Corporate'): Adjusted p-value = 1.9642241429667575e-07
('Consumer', 'Home Office'): Adjusted p-value = 7.026645491004073e-11
('Corporate', 'Home Office'): Adjusted p-value = 3.3795511931386933e-06

Post-hoc results for City with Segment:
('Consumer', 'Corporate'): Adjusted p-value = 3.94750895186823e-27
('Consumer', 'Home Office'): Adjusted p-value = 1.0096633663067795e-23
('Corporate', 'Home Office'): Adjusted p-value = 3.757551612400925e-11

Post-hoc results for Ship Mode with Segment:

('Consumer', 'Corporate'): Adjusted p-value = 0.0006284570132243212
('Consumer', 'Home Office'): Adjusted p-value = 0.8506425480165054
('Corporate', 'Home Office'): Adjusted p-value = 0.0015140818470504556

Post-hoc results for Order Month with Segment:
('Consumer', 'Corporate'): Adjusted p-value = 0.022012374707404657
('Consumer', 'Home Office'): Adjusted p-value = 7.460557644523636e-05
('Corporate', 'Home Office'): Adjusted p-value = 0.003405814771980744
"""

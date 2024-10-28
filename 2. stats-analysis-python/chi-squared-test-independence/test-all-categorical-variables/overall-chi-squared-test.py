import pandas as pd
from scipy.stats import chi2_contingency
import plotly.graph_objects as go

# Load the dataset
file_path = 'C:\\Users\\loydt\\Downloads\\Projects\\Superstore Sales Dataset.csv'
test_data = pd.read_csv(file_path)

# Convert 'Order Date' to datetime format if it's not already
test_data['Order Date'] = pd.to_datetime(test_data['Order Date'])

# Extract the month from the 'Order Date'
test_data['Order Month'] = test_data['Order Date'].dt.month

# Define the combinations for Chi-squared tests
combinations = {
    'Segment vs. Category': ('Segment', 'Category'),
    'State vs. Category': ('State', 'Category'),
    'City vs. Category': ('City', 'Category'),
    'Region vs. Category': ('Region', 'Category'),
    'Ship Mode vs. Category': ('Ship Mode', 'Category'),
    'Order Month vs. Category': ('Order Month', 'Category'),    
    'Category vs. Segment': ('Category', 'Segment'),
    'State vs. Segment': ('State', 'Segment'),
    'City vs. Segment': ('City', 'Segment'),
    'Region vs. Segment': ('Region', 'Segment'),
    'Ship Mode vs. Segment': ('Ship Mode', 'Segment'),
    'Order Month vs. Segment': ('Order Month', 'Segment'),
    'Segment vs. State': ('Segment', 'State'),
    'Category vs. State': ('Category', 'State'),
    'City vs. State': ('City', 'State'),
    'Region vs. State': ('Region', 'State'),
    'Ship Mode vs. State': ('Ship Mode', 'State'),
    'Order Month vs. State': ('Order Month', 'State'),
    'Segment vs. City': ('Segment', 'City'),
    'Category vs. City': ('Category', 'City'),
    'State vs. City': ('State', 'City'),
    'Region vs. City': ('Region', 'City'),
    'Ship Mode vs. City': ('Ship Mode', 'City'),
    'Order Month vs. City': ('Order Month', 'City'),
    'Segment vs. Region': ('Segment', 'Region'),
    'Category vs. Region': ('Category', 'Region'),
    'State vs. Region': ('State', 'Region'),
    'City vs. Region': ('City', 'Region'),
    'Ship Mode vs. Region': ('Ship Mode', 'Region'),
    'Order Month vs. Region': ('Order Month', 'Region'),
    'Segment vs. Ship Mode': ('Segment', 'Ship Mode'),
    'Category vs. Ship Mode': ('Category', 'Ship Mode'),
    'State vs. Ship Mode': ('State', 'Ship Mode'),
    'City vs. Ship Mode': ('City', 'Ship Mode'),
    'Region vs. Ship Mode': ('Region', 'Ship Mode'),
    'Order Month vs. Ship Mode': ('Order Month', 'Ship Mode'),
    'Segment vs. Order Month': ('Segment', 'Order Month'),
    'Category vs. Order Month': ('Category', 'Order Month'),
    'State vs. Order Month': ('State', 'Order Month'),
    'City vs. Order Month': ('City', 'Order Month'),
    'Region vs. Order Month': ('Region', 'Order Month'),
    'Ship Mode vs. Order Month': ('Order Month', 'Order Month')

}

# Perform Chi-squared tests for each combination
for combo_name, (var1, var2) in combinations.items():
    # Create the contingency table for the current combination
    contingency_table = pd.crosstab(test_data[var2], test_data[var1])
    print(f"\nContingency Table for {combo_name}:\n{contingency_table}")

    # Perform Chi-squared test without capturing statistic variables initially to check expected frequencies
    _, _, _, expected = chi2_contingency(contingency_table)

    # Check that all expected frequencies are >= 5
    if (expected < 5).sum() > 0:
        print("Warning: Some expected frequencies are less than 5, which may affect the test's reliability.")
    else:
        print("All expected frequencies are 5 or greater.")

    # Conduct the test and capture outputs
    chi2_stat, p_value, dof, expected = chi2_contingency(contingency_table)

    print(f"Chi-squared Statistic for {combo_name}: {chi2_stat}")
    print(f"P-value for {combo_name}: {p_value}")
    print(f"Degrees of Freedom for {combo_name}: {dof}")

    alpha = 0.05
    if p_value < alpha:
        print("Reject the null hypothesis: There is a significant association between", var1, "and", var2)
    else:
        print("Fail to reject the null hypothesis: There is no significant association between", var1, "and", var2)

    # Calculate residuals
    residuals = contingency_table.values - expected

    # Display residuals with their corresponding categories
    residuals_df = pd.DataFrame(
        residuals, 
        index=contingency_table.index, 
        columns=contingency_table.columns
    )
    print("\nResiduals (Observed - Expected) for", combo_name, ":\n", residuals_df)

    # Create a heatmap for the contingency table
    #fig = go.Figure(data=go.Heatmap(
    #    z=contingency_table.values,
    #    x=contingency_table.columns,
    #    y=contingency_table.index,
    #    colorscale='agsunset',
    #    text=contingency_table.values,
    #    texttemplate='%{text}',
    #    textfont=dict(color='white')
    #))

    # Customize layout
    #fig.update_layout(
    #    title=f'Contingency Table: {var1} vs {var2}',
    #    xaxis_title=var1,
    #    yaxis_title=var2,
    #    plot_bgcolor='grey',
    #    paper_bgcolor='black',
    #    font=dict(color='ghostwhite')
    #)

    # Show the plot
    #fig.show()

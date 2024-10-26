import pandas as pd
import math
import plotly.express as px
from scipy.stats import levene, bartlett, f_oneway
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Load the dataset
file_path = 'C:\\Users\\loydt\\Downloads\\Projects\\Superstore Sales Dataset.xlsx'
data = pd.read_excel(file_path)

# Filter the big four states generating higher sales
states_of_interest = [
    'Washington', 'California', 'New York', 'Florida', 'Pennsylvania'
]
state_data = data[data['State'].isin(states_of_interest)]

# Extracting columns to explore market insights
high_sales_states = state_data[[
    'Segment', 'State', 'City', 'Region', 'Ship Mode', 
    'Order Date', 'Category', 'Sub-Category', 
    'Product Name', 'Sales'
]]

# Step 1: Calculate the purchase frequency (or total sales) for each product
# within each sub-category and segment
product_counts = high_sales_states.groupby([
    'Sub-Category', 'Segment', 'Ship Mode', 
    'Region', 'Order Date', 'Product Name'
]).agg({'Sales': 'sum'}).reset_index()

# Step 2: Normalize the scores within each sub-category to get the 
# popularity score (scaled between 0 and 100)
product_counts['Popularity Score'] = product_counts.groupby(
    'Sub-Category'
)['Sales'].transform(lambda x: x / x.sum() * 100)

# Step 3: Merge the popularity scores back into the main DataFrame
high_sales_states = high_sales_states.merge(
    product_counts[['Sub-Category', 'Segment', 'Ship Mode', 
                    'Region', 'Order Date', 'Product Name', 
                    'Popularity Score']],
    on=['Sub-Category', 'Segment', 'Ship Mode', 
        'Region', 'Order Date', 'Product Name'],
    how='left'
)

# Step 4: Sort the products within each sub-category by popularity score
# in descending order
ranked_products = product_counts.sort_values(
    by=['Sub-Category', 'Popularity Score'], 
    ascending=[True, False]
)

# Take the logarithm of the Sales column and add it as a new column
high_sales_states['log_sales'] = high_sales_states['Sales'].apply(
    lambda x: math.log(x) if x > 0 else None
)

# Create boxplot for log-transformed sales by customer segment
boxplot_fig = px.box(
    high_sales_states, 
    x="Segment", 
    y="log_sales", 
    title="Log-Transformed Sales by Segment",
    labels={"Segment": "Customer Segment", "log_sales": "Log of Sales"},
    template="plotly_dark",  # Dark background template
)

# Show boxplot
boxplot_fig.show()

# Create histogram for log-transformed sales, faceted by customer segment
histogram_fig = px.histogram(
    high_sales_states,
    x="log_sales",
    facet_col="Segment",  # Separate histogram for each segment
    title="Log-Transformed Sales Distribution by Customer Segment",
    labels={"log_sales": "Log of Sales"},
    template="plotly_dark",  # Dark background template
)

# Show histogram plot
histogram_fig.show()

# Group the log-transformed sales data by customer segment
segments = [
    high_sales_states.loc[high_sales_states['Segment'] == segment, 'log_sales']
    for segment in high_sales_states['Segment'].unique()
]

# Levene's Test (robust to non-normality)
levene_stat, levene_p = levene(*segments)
print("Levene's Test Results:")
print(f"Statistic: {levene_stat}, P-value: {levene_p}")
if levene_p < 0.05:
    print("The variances across segments are significantly different "
          "(p < 0.05), indicating the assumption of homogeneity of variances is violated.\n")
else:
    print("The variances across segments are not significantly different "
          "(p >= 0.05), indicating the assumption of homogeneity of variances is met.\n")

# Bartlett's Test (sensitive to normality)
bartlett_stat, bartlett_p = bartlett(*segments)
print("Bartlett's Test Results:")
print(f"Statistic: {bartlett_stat}, P-value: {bartlett_p}")
if bartlett_p < 0.05:
    print("The variances across segments are significantly different "
          "(p < 0.05), indicating the assumption of homogeneity of variances is violated.\n")
else:
    print("The variances across segments are not significantly different "
          "(p >= 0.05), indicating the assumption of homogeneity of variances is met.\n")

# Fit an OLS model with log_sales as the dependent variable and Segment as the categorical predictor
model = ols("log_sales ~ C(Segment)", data=high_sales_states).fit()

# Display the summary to interpret coefficients
print(model.summary())

# Perform the ANOVA test
anova_result = f_oneway(*segments)

# Output the results
print("ANOVA Test Results:")
print(f"F-statistic: {anova_result.statistic}")
print(f"P-value: {anova_result.pvalue}")

# Interpretation
if anova_result.pvalue < 0.05:
    print("Reject the null hypothesis: There are significant differences between the segments.")
else:
    print("Fail to reject the null hypothesis: There are no significant differences between the segments.")

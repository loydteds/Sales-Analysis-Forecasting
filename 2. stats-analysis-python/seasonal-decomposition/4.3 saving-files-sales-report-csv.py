import pandas as pd
import statsmodels.api as sm
import plotly.graph_objs as go
import os

class SalesPerformanceEvaluator:
    def __init__(self, file_path, output_dir, sub_categories):
        self.file_path = file_path
        self.output_dir = output_dir
        self.sub_categories = sub_categories
        self.data = self.load_data()
        os.makedirs(self.output_dir, exist_ok=True)

    def load_data(self):
        """Load and prepare the dataset."""
        data = pd.read_excel(self.file_path)
        data['Order Date'] = pd.to_datetime(data['Order Date'], format='%d/%m/%Y', errors='coerce')
        data.set_index('Order Date', inplace=True)
        return data

    def resample_monthly_sales(self, sub_category_data):
        """Resample sales data to monthly sums."""
        return sub_category_data['Sales'].resample('ME').sum()

    def perform_seasonal_decomposition(self, monthly_sales):
        """Perform seasonal decomposition on monthly sales data."""
        return sm.tsa.seasonal_decompose(monthly_sales, model='additive', period=12)

    def get_seasonal_and_residual(self, decomposition):
        """Extract seasonal and residual components."""
        return decomposition.seasonal, decomposition.resid

    def collect_expected_values(self, seasonal, residual):
        """Collect expected increases, drops, and record residual values."""
        expected_increases = []
        expected_drops = []
        recorded_values = {date.date(): residual_value for date, residual_value in zip(residual.index, residual) if pd.notna(residual_value)}
        
        for date, seasonal_value in zip(seasonal.index, seasonal):
            if pd.notna(seasonal_value):
                if seasonal_value > 0:
                    expected_increases.append((date.date(), seasonal_value))
                elif seasonal_value < 0:
                    expected_drops.append((date.date(), seasonal_value))
        
        return expected_increases, expected_drops, recorded_values

    def evaluate_performance(self, expected_values, recorded_values, expectation_type):
        """Evaluate performance based on expected values and recorded residual values."""
        results = []
        total_failed_expectations = 0
        total_exceeded_expectations = 0

        for date, expected_value in expected_values:
            recorded_value = recorded_values.get(date)
            if recorded_value is not None:
                if expected_value > 0 and recorded_value < expected_value:
                    failed_expectations = abs(expected_value - recorded_value)
                    total_failed_expectations += failed_expectations
                    results.append([date, expectation_type, expected_value, recorded_value, "Failed", failed_expectations])
                elif expected_value > 0 and recorded_value > expected_value:
                    exceeded_expectations = abs(recorded_value - expected_value)
                    total_exceeded_expectations += exceeded_expectations
                    results.append([date, expectation_type, expected_value, recorded_value, "Exceeded", exceeded_expectations])

        return results, total_failed_expectations, total_exceeded_expectations

    def save_results(self, results, sub_category):
        """Save the performance results to a CSV file."""
        results_df = pd.DataFrame(results, columns=["Date", "Expectation Type", "Expected Value", "Recorded Value", "Status", "Value Difference"])
        results_df.to_csv(os.path.join(self.output_dir, f"{sub_category}_Sales_Performance.csv"), index=False)

    def evaluate_sub_category(self, sub_category):
        """Evaluate sales performance for each sub-category."""
        sub_category_data = self.data[self.data['Sub-Category'] == sub_category]
        monthly_sales = self.resample_monthly_sales(sub_category_data)
        decomposition = self.perform_seasonal_decomposition(monthly_sales)
        seasonal, residual = self.get_seasonal_and_residual(decomposition)
        
        expected_increases, expected_drops, recorded_values = self.collect_expected_values(seasonal, residual)
        
        increase_results, total_failed_increases, total_exceeded_increases = self.evaluate_performance(expected_increases, recorded_values, "Expected Increase")
        drop_results, total_failed_drops, total_exceeded_drops = self.evaluate_performance(expected_drops, recorded_values, "Expected Drop")
        
        total_results = increase_results + drop_results
        total_results.append(["Total", "N/A", "N/A", "N/A", "Expected Increase but Failed Total", total_failed_increases])
        total_results.append(["Total", "N/A", "N/A", "N/A", "Expected Increase and Exceeded Total", total_exceeded_increases])
        total_results.append(["Total", "N/A", "N/A", "N/A", "Expected Drop but Failed Total", total_failed_drops])
        total_results.append(["Total", "N/A", "N/A", "N/A", "Expected Drop and Exceeded Total", total_exceeded_drops])

        self.save_results(total_results, sub_category)

    def run(self):
        """Run performance evaluation for all sub-categories."""
        for sub_category in self.sub_categories:
            self.evaluate_sub_category(sub_category)
        print("Performance evaluation files saved for each sub-category.")


# Usage example
file_path = 'C:\\Users\\loydt\\Downloads\\Projects\\Superstore Sales Dataset.xlsx'
output_dir = 'Sales_Performance_Results'
sub_categories = ['Bookcases', 'Chairs', 'Labels', 'Tables', 'Storage', 'Furnishings', 
                  'Art', 'Phones', 'Binders', 'Appliances', 'Paper', 'Accessories', 
                  'Envelopes', 'Fasteners', 'Supplies', 'Machines', 'Copiers']

evaluator = SalesPerformanceEvaluator(file_path, output_dir, sub_categories)
evaluator.run()

import pandas as pd
from scipy.stats import chi2_contingency
import plotly.graph_objects as go


class DataLoader:
    """Handles data loading and preprocessing tasks."""
    
    @staticmethod
    def load_data(file_path: str) -> pd.DataFrame:
        """Loads dataset from CSV and processes datetime columns."""
        data = pd.read_csv(file_path)
        data['Order Date'] = pd.to_datetime(data['Order Date'])
        data['Order Month'] = data['Order Date'].dt.month
        return data


class ChiSquaredTest:
    """Performs the Chi-squared test and handles contingency tables."""
    
    def __init__(self, data: pd.DataFrame, var1: str, var2: str):
        self.data = data
        self.var1 = var1
        self.var2 = var2
        self.contingency_table = pd.crosstab(data[var2], data[var1])
        self.alpha = 0.05

    def perform_test(self):
        """Performs the Chi-squared test and outputs results."""
        chi2_stat, p_value, dof, expected = chi2_contingency(self.contingency_table)
        print(f"\nContingency Table for {self.var1} vs {self.var2}:\n{self.contingency_table}")
        print(f"Chi-squared Statistic: {chi2_stat}")
        print(f"P-value: {p_value}")
        print(f"Degrees of Freedom: {dof}")
        
        self._check_expected_frequencies(expected)
        self._interpret_results(p_value)

    def _check_expected_frequencies(self, expected):
        """Checks if expected frequencies meet assumptions."""
        if (expected < 5).sum() > 0:
            print("Warning: Some expected frequencies are less than 5, which may affect the test's reliability.")
        else:
            print("All expected frequencies are 5 or greater.")

    def _interpret_results(self, p_value):
        """Interprets the test result based on the p-value."""
        if p_value < self.alpha:
            print(f"Reject the null hypothesis: There is a significant association between {self.var1} and {self.var2}")
        else:
            print(f"Fail to reject the null hypothesis: There is no significant association between {self.var1} and {self.var2}")

    def calculate_residuals(self, expected):
        """Calculates and prints residuals between observed and expected values."""
        residuals = self.contingency_table.values - expected
        residuals_df = pd.DataFrame(residuals, index=self.contingency_table.index, columns=self.contingency_table.columns)
        print(f"\nResiduals (Observed - Expected) for {self.var1} vs {self.var2}:\n{residuals_df}")


class DataVisualizer:
    """Handles data visualization for Chi-squared test results."""
    
    @staticmethod
    def create_heatmap(contingency_table: pd.DataFrame):
        """Creates and displays a heatmap for the contingency table."""
        fig = go.Figure(data=go.Heatmap(
            z=contingency_table.values,
            x=contingency_table.columns,
            y=contingency_table.index,
            colorscale='agsunset',
            text=contingency_table.values,
            texttemplate='%{text}',
            textfont=dict(color='white')
        ))

        fig.update_layout(
            title=f'Contingency Table: {contingency_table.columns[0]} vs {contingency_table.index[0]}',
            xaxis_title=contingency_table.columns[0],
            yaxis_title=contingency_table.index[0],
            plot_bgcolor='grey',
            paper_bgcolor='black',
            font=dict(color='ghostwhite')
        )
        
        fig.show()


class ChiSquaredAnalysis:
    """Main class to manage the Chi-squared analysis workflow."""
    
    def __init__(self, file_path: str):
        self.data = DataLoader.load_data(file_path)
        self.combinations = self._define_combinations()

    def _define_combinations(self):
        """Defines the variable pairs for Chi-squared tests."""
        return {
            'Segment vs. Category': ('Segment', 'Category'),
            'State vs. Category': ('State', 'Category'),
            # Add more combinations as needed
        }

    def perform_analysis(self):
        """Performs Chi-squared tests for each variable combination."""
        for combo_name, (var1, var2) in self.combinations.items():
            test = ChiSquaredTest(self.data, var1, var2)
            test.perform_test()
            test.calculate_residuals(test.contingency_table.values)
            DataVisualizer.create_heatmap(test.contingency_table)


# Execute the analysis
file_path = 'C:\\Users\\loydt\\Downloads\\Projects\\Superstore Sales Dataset.csv'
analysis = ChiSquaredAnalysis(file_path)
analysis.perform_analysis()

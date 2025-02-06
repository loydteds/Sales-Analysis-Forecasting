import pandas as pd
import math
import plotly.express as px
from scipy.stats import levene, bartlett, f_oneway
from abc import ABC, abstractmethod

class DataProcessor:
    def __init__(self, file_path: str):
        self.data = pd.read_excel(file_path)
    
    def filter_states(self, states):
        return self.data[self.data['State'].isin(states)].copy()

    def log_transform_sales(self, df, column='Sales'):
        df['log_sales'] = df[column].apply(lambda x: math.log(x) if x > 0 else None)
        return df

class StatisticalTests(ABC):
    def __init__(self, data, column):
        self.data = data
        self.column = column
        self.groups = [self.data.loc[self.data[self.column] == value, 'log_sales'].dropna() 
                       for value in self.data[self.column].unique()]

    @abstractmethod
    def run_test(self):
        pass

class LeveneTest(StatisticalTests):
    def run_test(self):
        stat, p = levene(*self.groups)
        print(f"Levene's Test Results for {self.column}: Statistic = {stat}, P-value = {p}")
        print("Variances are" + (" significantly different." if p < 0.05 else " not significantly different."))

class BartlettTest(StatisticalTests):
    def run_test(self):
        stat, p = bartlett(*self.groups)
        print(f"Bartlett's Test Results for {self.column}: Statistic = {stat}, P-value = {p}")
        print("Variances are" + (" significantly different." if p < 0.05 else " not significantly different."))

class AnovaTest(StatisticalTests):
    def run_test(self):
        result = f_oneway(*self.groups)
        print(f"ANOVA Test Results for {self.column}: F-statistic = {result.statistic}, P-value = {result.pvalue}")
        print("Reject the null hypothesis." if result.pvalue < 0.05 else "Fail to reject the null hypothesis.")

class DataVisualizer:
    @staticmethod
    def generate_boxplots(data, columns):
        for column in columns:
            fig = px.box(
                data, x=column, y="log_sales", title=f"Log-Transformed Sales by {column}",
                labels={column: column, "log_sales": "Log of Sales"}, template="plotly_dark"
            )
            fig.show()

# Execution
file_path = 'C:\\Users\\loydt\\Downloads\\Projects\\Superstore Sales Dataset.xlsx'
states_of_interest = ['Washington', 'California', 'New York', 'Florida', 'Pennsylvania']

processor = DataProcessor(file_path)
data = processor.filter_states(states_of_interest)
data = processor.log_transform_sales(data)

columns_to_test = ['Sub-Category', 'Category', 'State', 'Segment', 'Ship Mode', 'Region']
DataVisualizer.generate_boxplots(data, columns_to_test)

for column in columns_to_test:
    LeveneTest(data, column).run_test()
    BartlettTest(data, column).run_test()
    AnovaTest(data, column).run_test()

print("Data Processing and Statistical Analysis Complete!")

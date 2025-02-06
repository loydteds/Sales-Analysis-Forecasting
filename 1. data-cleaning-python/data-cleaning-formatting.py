import pandas as pd
import re
from abc import ABC, abstractmethod

class DataCleaner(ABC):
    def __init__(self, data: pd.Series):
        self.data = data
        self.cleaned_data = self.clean_extra_spaces()
    
    def clean_extra_spaces(self):
        return self.data.astype(str).str.strip().str.replace(r'\s+', ' ', regex=True)

    @abstractmethod
    def validate(self):
        pass
    
    def check_missing_values(self):
        missing_count = self.cleaned_data.isnull().sum()
        print(f"Missing Values: {missing_count}")
    
    def check_extra_spaces(self):
        extra_spaces = self.data[self.data.str.contains(r'^\s+|\s{2,}|\s+$', regex=True)]
        if not extra_spaces.empty:
            print("Entries with Extra Spaces:")
            print(extra_spaces)
        else:
            print("No Extra Spaces Detected")

class OrderIDCleaner(DataCleaner):
    def validate(self):
        pattern = r"^(CA|US)-\d{4}-1\d{5}$"
        invalid_ids = self.cleaned_data[~self.cleaned_data.str.match(pattern)]
        print("Invalid Order IDs:")
        print(invalid_ids if not invalid_ids.empty else "All Order IDs are valid.")

class DateCleaner(DataCleaner):
    def validate(self):
        pattern = r"^\d{4}-\d{2}-\d{2}$"
        invalid_dates = self.cleaned_data[~self.cleaned_data.str.match(pattern)]
        print("Invalid Dates:")
        print(invalid_dates if not invalid_dates.empty else "All Dates are valid.")

class CategoryCleaner(DataCleaner):
    def validate(self):
        pattern = r"^(Consumer|Corporate|Home Office)$"
        invalid_categories = self.cleaned_data[~self.cleaned_data.str.match(pattern)]
        print("Invalid Categories:")
        print(invalid_categories if not invalid_categories.empty else "All Categories are valid.")

# Load Data
data = pd.read_csv('C:\\Users\\loydt\\Downloads\\Projects\\Superstore Sales Dataset.csv')

# Apply Cleaners
order_id_cleaner = OrderIDCleaner(data['Order ID'])
order_id_cleaner.validate()
order_id_cleaner.check_missing_values()
order_id_cleaner.check_extra_spaces()

order_date_cleaner = DateCleaner(data['Order Date'])
order_date_cleaner.validate()
order_date_cleaner.check_missing_values()
order_date_cleaner.check_extra_spaces()

category_cleaner = CategoryCleaner(data['Segment'])
category_cleaner.validate()
category_cleaner.check_missing_values()
category_cleaner.check_extra_spaces()

print("Data Cleaning Complete!")

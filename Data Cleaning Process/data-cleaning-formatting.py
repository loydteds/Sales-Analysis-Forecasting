import pandas as pd

# Step 1: Load the dataset
file_path = 'C:\\Users\\loydt\\Downloads\\Projects\\Superstore Sales Dataset.csv'  # Your file path
data = pd.read_csv(file_path)

# Step 2: Extract the 'Order ID' column directly as a pandas Series
order_id = data['Order ID']

# Function to clean extra spaces
def clean_extra_spaces(order_id):
    orderid_series_cleaned = order_id.str.strip().str.replace(r'\s+', ' ', regex=True)
    return orderid_series_cleaned

# Step 3: Define the DataValidation class and validation method
class OrderIDValidation:
    def __init__(self, order_id):
        self.order_id = clean_extra_spaces(order_id)

    # Method to validate 'Order ID' format
    def order_id_validation(self):
        # Define the regex pattern for the standard format (CA/US-year-6digit)
        pattern = r"^(CA|US)-\d{4}-1\d{5}$"
        
        # Create a boolean Series that indicates whether each order ID matches the pattern
        valid_order_ids = self.order_id.str.match(pattern)

        # Create a DataFrame with invalid IDs using boolean indexing
        invalid_ids_df = self.order_id[~valid_order_ids].to_frame(name='Order ID')

        # Print the invalid IDs DataFrame or confirm no discrepancy
        if not invalid_ids_df.empty:
            print("Standard Order ID: NO")
            print(invalid_ids_df)
        else:
            print("Standard Order ID: YES")

    # Method to check for missing values in the 'Order ID' column 
    def check_missing_id(self):
        # Count the missing values in the 'Order ID' column
        missing_values = self.order_id.isnull().sum()
        # Print the number of missing values
        print(f"\nMissing Values Order ID: {missing_values}")

    # Define pattern for extra spaces
    pattern_extra_spaces_orderid = r'^\s+|\s{2,}|\s+$' 
    
    # Method to check for extra spaces
    def check_extra_spaces(self):
        # Use the cleaned segment directly, no need to convert to pd.Series
        orderid_extra_spaces = self.order_id

        # Create a boolean mask for extra spaces
        orderid_with_extra_spaces = orderid_extra_spaces[orderid_extra_spaces.str.contains(self.pattern_extra_spaces_orderid, regex=True)]

        if not orderid_with_extra_spaces.empty:
            print("\nOrder IDs with Extra Spaces:")
            print(orderid_with_extra_spaces)  # Print the variable correctly
        else:
            print("\nNo Extra Spaces Detected")

# Step 4: Create an instance of the OrderIDValidation class and pass the 'Order ID' data
data_validation = OrderIDValidation(order_id)

# Step 5: Apply the validation method
data_validation.order_id_validation()
data_validation.check_missing_id()
data_validation.check_extra_spaces()

# Extract the 'Order Date' column directly as a pandas Series
order_date = data['Order Date'] 

# Function to clean extra spaces
def clean_extra_spaces(order_date):
    orderdate_series_cleaned = order_date.str.strip().str.replace(r'\s+', ' ', regex=True)
    return orderdate_series_cleaned    

# Defining the OrderDateFormat class and validation method
class OrderDateFormat:
    def __init__(self, order_date):
        self.order_date = clean_extra_spaces(order_date)  # Clean the dates on initialization
        self.invalid_order_dates = pd.Series(dtype='object')  # Initialize an empty Series for invalid dates

    # Method to check missing dates
    def check_missing_dates(self):
        missing_dates = self.order_date.isnull().sum()
        print(f"\nMissing Values Order Date: {missing_dates}")

    # Define valid date formats using regex patterns
    def date_validation(self):
        # Define the regex pattern for the standard date format 'yyyy-dd-mm'
        valid_date_pattern = r"^\d{4}-\d{2}-\d{2}$"

        # Create a boolean Series that indicates whether each order date matches the pattern 
        valid_order_dates = self.order_date.str.match(valid_date_pattern)

        # Create a DataFrame with invalid dates using boolean indexing
        self.invalid_order_dates = self.order_date[~valid_order_dates].to_frame(name='Order Date')

        # Print the invalid order dates
        if not self.invalid_order_dates.empty:
            print("\nInitial Assessment:\n")
            print("Standard Order Date: NO\n")
            print(self.invalid_order_dates)
        else:
            print("\nInitial Assessment\n")
            print("\nStandard Order Date: YES\n")

    # Define pattern for extra spaces
    pattern_extra_spaces_orderdate = r'^\s+|\s{2,}|\s+$' 
    
    # Method to check for extra spaces
    def check_extra_spaces(self):
        # Use the cleaned segment directly
        orderdate_extra_spaces = self.order_date

        # Create a boolean mask for extra spaces
        orderdate_with_extra_spaces = orderdate_extra_spaces[orderdate_extra_spaces.str.contains(self.pattern_extra_spaces_orderdate, regex=True)]

        if not orderdate_with_extra_spaces.empty:
            print("\nOrder Date with Extra Spaces:")
            print(orderdate_with_extra_spaces)  # Print the variable correctly
        else:
            print("\nNo Extra Spaces Detected")
    
    # Method to transform invalid dates to valid date format
    def date_formatting(self):
        print("\nFinal Assessment:\n")
        # Ensure invalid_order_dates is available
        if not self.invalid_order_dates.empty:
            # Initialize a list to store valid formatted dates
            formatted_dates = []

            # Iterate through each invalid date
            for date in self.invalid_order_dates['Order Date']:
                # Attempt to extract day, month, and year
                try:
                    # Assuming dates are initially in 'dd-mm-yyyy' format or 'mm-dd-yyyy'
                    if '-' in date:  # Check if date has dashes
                        parts = date.split('-')
                        if len(parts) == 3:
                            # Adjust based on expected format
                            day, month, year = map(int, parts)  # Convert to integers

                            # Check if the day and month are within valid ranges
                            if 1 <= day <= 31 and 1 <= month <= 12:
                                # Format the date to 'yyyy-dd-mm'
                                formatted_date = f"{year}-{day:02d}-{month:02d}"
                                formatted_dates.append(formatted_date)
                            else:
                                print(f"Invalid date detected: {date} (Day: {day}, Month: {month})")
                        else:
                            print(f"Unexpected date format: {date}")
                    else:
                        print(f"Invalid date format (no dashes): {date}")

                except ValueError:
                    print(f"Error processing date: {date}")

            # Create a DataFrame to store the newly formatted valid dates
            if formatted_dates:
                # Combine the valid dates with original data for output
                formatted_dates_df = pd.DataFrame(formatted_dates, columns=['Formatted Order Date'])
                print(f"\nFormatted Dates:\n{formatted_dates_df}")
                # Print the count of formatted dates
                print(f"\nTotal Formatted Dates: {len(formatted_dates)}")
        else:
            print("\nDates are Valid.")

# Create an instance of the OrderDateFormat class and pass the 'Order Date' data
date_transformation = OrderDateFormat(order_date)

# Apply the missing dates validation
date_transformation.check_missing_dates()
date_transformation.date_validation()
date_transformation.date_formatting()
date_transformation.check_extra_spaces()

# Extract the 'Ship Date' column directly as a pandas Series
ship_date = data['Ship Date'] 

# Function to clean extra spaces
def clean_extra_spaces(ship_date):
    shipdate_series_cleaned = ship_date.str.strip().str.replace(r'\s+', ' ', regex=True)
    return shipdate_series_cleaned    

# Defining the ShipDateFormat class and validation method
class ShipDateFormat:
    def __init__(self, ship_date):
        self.ship_date = clean_extra_spaces(ship_date)  # Clean the dates on initialization
        self.invalid_ship_dates = pd.Series(dtype='object')  # Initialize an empty Series for invalid dates

    # Method to check missing dates
    def check_missing_dates(self):
        missing_dates = self.ship_date.isnull().sum()
        print(f"\nMissing Values Ship Date: {missing_dates}")

    # Define valid date formats using regex patterns
    def date_validation(self):
        # Define the regex pattern for the standard date format 'yyyy-dd-mm'
        valid_date_pattern = r"^\d{4}-\d{2}-\d{2}$"

        # Create a boolean Series that indicates whether each order date matches the pattern 
        valid_order_dates = self.ship_date.str.match(valid_date_pattern)

        # Create a DataFrame with invalid dates using boolean indexing
        self.invalid_ship_dates = self.ship_date[~valid_order_dates].to_frame(name='Ship Date')

        # Print the invalid order dates
        if not self.invalid_ship_dates.empty:
            print("\nInitial Assessment:\n")
            print("Standard Ship Date: NO\n")
            print(self.invalid_ship_dates)
        else:
            print("\nInitial Assessment\n")
            print("\nStandard Ship Date: YES\n")

    # Define pattern for extra spaces
    pattern_extra_spaces_shipdate = r'^\s+|\s{2,}|\s+$' 
    
    # Method to check for extra spaces
    def check_extra_spaces(self):
        # Use the cleaned segment directly
        shipdate_extra_spaces = self.ship_date

        # Create a boolean mask for extra spaces
        shipdate_with_extra_spaces = shipdate_extra_spaces[shipdate_extra_spaces.str.contains(self.pattern_extra_spaces_shipdate, regex=True)]

        if not shipdate_with_extra_spaces.empty:
            print("\nShip Date with Extra Spaces:")
            print(shipdate_with_extra_spaces)  # Print the variable correctly
        else:
            print("\nNo Extra Spaces Detected")
    
    # Method to transform invalid dates to valid date format
    def date_formatting(self):
        print("\nFinal Assessment:\n")
        # Ensure invalid_ship_dates is available
        if not self.invalid_ship_dates.empty:
            # Initialize a list to store valid formatted dates
            formatted_dates = []

            # Iterate through each invalid date
            for date in self.invalid_ship_dates['Ship Date']:
                # Attempt to extract day, month, and year
                try:
                    # Assuming dates are initially in 'dd-mm-yyyy' format or 'mm-dd-yyyy'
                    if '-' in date:  # Check if date has dashes
                        parts = date.split('-')
                        if len(parts) == 3:
                            # Adjust based on expected format
                            day, month, year = map(int, parts)  # Convert to integers

                            # Check if the day and month are within valid ranges
                            if 1 <= day <= 31 and 1 <= month <= 12:
                                # Format the date to 'yyyy-dd-mm'
                                formatted_date = f"{year}-{day:02d}-{month:02d}"
                                formatted_dates.append(formatted_date)
                            else:
                                print(f"Invalid date detected: {date} (Day: {day}, Month: {month})")
                        else:
                            print(f"Unexpected date format: {date}")
                    else:
                        print(f"Invalid date format (no dashes): {date}")

                except ValueError:
                    print(f"Error processing date: {date}")

            # Create a DataFrame to store the newly formatted valid dates
            if formatted_dates:
                # Combine the valid dates with original data for output
                formatted_dates_df = pd.DataFrame(formatted_dates, columns=['Formatted Ship Date'])
                print(f"\nFormatted Dates:\n{formatted_dates_df}")
                # Print the count of formatted dates
                print(f"\nTotal Formatted Dates: {len(formatted_dates)}")
        else:
            print("\nDates are Valid.")

# Create an instance of the ShipDateFormat class and pass the 'Ship Date' data
date_transformation = ShipDateFormat(ship_date)

# Apply the missing dates validation
date_transformation.check_missing_dates()
date_transformation.date_validation()
date_transformation.date_formatting()
date_transformation.check_extra_spaces()

# Extract the 'Ship Mode' column directly as a pandas Series
ship_mode = data['Ship Mode']

# Function to clean extra spaces
def clean_extra_spaces(ship_mode):
    shipmode_series_cleaned = ship_mode.str.strip().str.replace(r'\s+', ' ', regex=True)
    return shipmode_series_cleaned   

# Defining the CategoryFormatting class and validation method
class CategoryFormat:
    def __init__(self, ship_mode):
        self.ship_mode = clean_extra_spaces(ship_mode)

    # Method to check missing dates
    def check_missing_ship_modes(self):
        missing_ship_data = self.ship_mode.isnull().sum()
        print(f"\nMissing Values Ship Mode: {missing_ship_data}")

    # Method to validate correct categories
    def ship_mode_validation(self):
        # Define the regex pattern for the standard ship mode category
        valid_ship_mode_pattern = r"^(Second Class|Standard Class|First Class|Same Day)$"

        # Create a boolean series to check the values if they match the patterns
        valid_ship_mode_categories = self.ship_mode.str.match(valid_ship_mode_pattern)

        # Create a DataFrame with invalid categories using boolean indexing
        invalid_ship_mode_categories = self.ship_mode[~valid_ship_mode_categories].to_frame(name="Ship Mode")

        # Print the invalide categories
        if not invalid_ship_mode_categories.empty:
            print("Standard Ship Mode: NO")
            print(invalid_ship_mode_categories)
        else:
            print("\nStandard Ship Mode: YES")

    # Define pattern for extra spaces
    pattern_extra_spaces_shipmode = r'^\s+|\s{2,}|\s+$' 
    
    # Method to check for extra spaces
    def check_extra_spaces(self):

        shipmode_extra_spaces = self.ship_mode

        # Create a boolean mask for extra spaces
        shipmode_with_extra_spaces = shipmode_extra_spaces[shipmode_extra_spaces.str.contains(self.pattern_extra_spaces_shipmode, regex=True)]

        if not shipmode_with_extra_spaces.empty:
            print("\nShip Mode with Extra Spaces:")
            print(shipmode_with_extra_spaces)  # Print the variable correctly
        else:
            print("\nNo Extra Spaces Detected")

# Create an instance of the CategoryFormat class and pass the 'Ship Mode' data
data_validation = CategoryFormat(ship_mode)

data_validation.check_missing_ship_modes()
data_validation.ship_mode_validation()
data_validation.check_extra_spaces()

# Extract the 'Customer ID' column
customer_ids = data['Customer ID']

# Extract the unique 'Customer ID' values
unique_customer_ids = pd.Series(customer_ids.unique())

# Function to clean extra spaces
def clean_extra_spaces(customer_ids):
    customerid_series_cleaned = customer_ids.str.strip().str.replace(r'\s+', ' ', regex=True)
    return customerid_series_cleaned

# Define the regex pattern for 'Customer ID'
customer_id_pattern = r"^[A-Z]{2}-\d{5}$"

# Validate 'Customer ID' using the regex pattern
def customer_id_validation(customer_ids):
    # Convert the array to a pandas Series (to use .str methods)
    customer_ids_series = pd.Series(customer_ids)
    
    # Create a boolean mask for invalid customer IDs
    invalid_customer_ids = customer_ids_series[~customer_ids_series.str.match(customer_id_pattern)]

    if not invalid_customer_ids.empty:
        print("Standard Customer IDs: NO")
        print(invalid_customer_ids)
    else:
        print("Standard Customer IDs: YES")

# Define the regex pattern for extra spaces
pattern_extra_spaces_customerid = r'(?:^\s+|\s{2,}|\s+$)'

# Method to check for extra spaces
def check_extra_spaces(customer_ids):
    customerid_extra_spaces = pd.Series(customer_ids)

    # Create a boolean mask for extra spaces
    customerid_with_extra_spaces = customerid_extra_spaces[customerid_extra_spaces.str.contains(pattern_extra_spaces_customerid, regex=True)]
    
    if not customerid_with_extra_spaces.empty:
        print("\nCustomer IDs with Extra Spaces")
        print(customerid_with_extra_spaces)
    else:
        print("\nNo Extra Spaces Detected")

# Method to check missing dates
def check_missing_customer_id(customer_ids):
        missing_ship_data = customer_ids.isnull().sum()
        print(f"\nMissing Customer IDs: {missing_ship_data}")

# Apply the validation to unique customer IDs
customer_id_validation(unique_customer_ids)

# Apply the method to check missing customer id's
check_missing_customer_id(customer_ids)

# Check for extra spaces
check_extra_spaces(customer_ids)

# Extract the 'Customer Name' column
customer_names = data['Customer Name']

# Extract the unique 'Customer Name' values
unique_customer_names = pd.Series(customer_names.unique())

# Function to clean extra spaces
def clean_extra_spaces(customer_names):
    customer_series_cleaned = customer_names.str.strip().str.replace(r'\s+', ' ', regex=True)
    return customer_series_cleaned   

# Define the regex pattern for valid customer names
customer_name_pattern_with_apostrophe = r"^[A-Za-z\s']{2,}$"
customer_name_pattern_without_apostrophe = r"^[A-Za-z\s]{2,}$"

# Validate 'Customer Name' using the regex pattern
def customer_name_validation(customer_names):
    # Convert the array to a pandas Series (to use .str methods)
    customer_names_series = clean_extra_spaces(customer_names)
    
    # Create a boolean mask for invalid customer names
    invalid_customer_names = customer_names_series[~customer_names_series.str.match(customer_name_pattern_with_apostrophe) & 
                                                    ~customer_names_series.str.match(customer_name_pattern_without_apostrophe)]

    if not invalid_customer_names.empty:
        print("\nInvalid Customer Names:")
        print(invalid_customer_names)
    else:
        print("\nValid Customer Names: YES")

# Define pattern for extra spaces
    pattern_extra_spaces_customer = r'^\s+|\s{2,}|\s+$' 
    
    # Method to check for extra spaces
    def check_extra_spaces(customer_names):
        # Use the cleaned segment directly, no need to convert to pd.Series
        customer_extra_spaces = pd.Series

        # Create a boolean mask for segment categories with extra spaces
        customer_with_extra_spaces = customer_extra_spaces[customer_extra_spaces.str.contains(pattern_extra_spaces_customer, regex=True)]

        if not customer_with_extra_spaces.empty:
            print("\nCustomer Names with Extra Spaces:")
            print(customer_with_extra_spaces)  # Print the variable correctly
        else:
            print("\nNo Extra Spaces Detected")

# Method to check missing names
def check_missing_customer_names(customer_names):
    missing_customer_names = customer_names.isnull().sum()
    print(f"\nMissing Customer Names: {missing_customer_names}")

# Apply the validation to unique customer names
customer_name_validation(unique_customer_names)

# Apply the method to check missing customer names
check_missing_customer_names(customer_names)

# Check for extra spaces
check_extra_spaces(customer_names) 

# Extract the 'Ship Mode' column directly as a pandas Series
segment = data['Segment']

# Function to clean extra spaces
def clean_extra_spaces(segment):
    segment_series_cleaned = segment.str.strip().str.replace(r'\s+', ' ', regex=True)
    return segment_series_cleaned         

# Defining the CategoryFormatting class and validation method
class CategoryFormat:
    def __init__(self, segment):
        self.segment = clean_extra_spaces(segment)

    # Method to check missing dates
    def check_missing_segment(self):
        missing_segment = self.segment.isnull().sum()
        print(f"\nShip Mode Missing Values: {missing_segment}")

    # Method to validate correct categories
    def segment_validation(self):
        # Define the regex pattern for the standard ship mode category
        valid_segment_format = r"^(Consumer|Corporate|Home Office)$"

        # Create a boolean series to check the values if they match the patterns
        valid_segment_categories = self.segment.str.match(valid_segment_format)

        # Create a DataFrame with invalid categories using boolean indexing
        invalid_segment_categories = self.segment[~valid_segment_categories].to_frame(name="Segment")

        # Print the invalide categories
        if not invalid_segment_categories.empty:
            print("Standard Ship Mode: NO")
            print(invalid_segment_categories)
        else:
            print("\nStandard Ship Mode: YES")
    
    # Define pattern for extra spaces
    pattern_extra_spaces_segment = r'^\s+|\s{2,}|\s+$' 
    
    # Method to check for extra spaces
    def check_extra_spaces(self):
        segment_extra_spaces = self.segment

        # Create a boolean mask for segment categories with extra spaces
        segment_with_extra_spaces = segment_extra_spaces[segment_extra_spaces.str.contains(self.pattern_extra_spaces_segment, regex=True)]

        if not segment_with_extra_spaces.empty:
            print("\nSegments with Extra Spaces")
            print("segment_with_extra_spaces")
        else:
            print("\nNo Extra Spaces Detected")

# Create an instance of the CategoryFormat class and pass the 'Ship Mode' data
data_validation = CategoryFormat(segment)

data_validation.check_missing_segment()
data_validation.segment_validation()
data_validation.check_extra_spaces()

# Extract the 'City' column
city = data['City']

# Extract the unique 'Customer Name' values
unique_city = pd.Series(city.unique())

# Function to clean extra spaces
def clean_extra_spaces(city):
    city_series_cleaned = city.str.strip().str.replace(r'\s+', ' ', regex=True)
    return city_series_cleaned

# Define the regex pattern for valid city names
pattern = r'^[A-Za-z ]+$'

# Validate 'City' using the regex pattern
def city_validation(city):
    # Convert the array to a pandas Series (to use .str methods)
    city_names = clean_extra_spaces(city)
    
    # Create a boolean mask for invalid city names
    invalid_city_names = city_names[~city_names.str.match(pattern)]

    if not invalid_city_names.empty:
        print("Invalid City Names:")
        print(invalid_city_names)
    else:
        print("Valid City Names: YES")

# Define the regex pattern for extra spaces
pattern_extra_spaces_city = r'(?:^\s+|\s{2,}|\s+$)'

# Method to check missing names
def check_missing_city_names(city):
    missing_city_names = city.isnull().sum()
    print(f"\nMissing City Names: {missing_city_names}")

# Method to check for extra spaces
def check_extra_spaces(city):
    city_extra_spaces = pd.Series(city)

    # Create a boolean mask for city names with extra spaces
    city_with_extra_spaces = city_extra_spaces[city_extra_spaces.str.contains(pattern_extra_spaces_city, regex=True)]
    
    if not city_with_extra_spaces.empty:
        print("\nCity Names with Extra Spaces")
        print(city_with_extra_spaces)
    else:
        print("\nNo Extra Spaces Detected")

# Apply the validation to unique city names
city_validation(unique_city)

# Apply the method to check missing city names
check_missing_city_names(city)

# Check for extra spaces
check_extra_spaces(city)

# Extract the 'State' column
state = data['State']

# Extract the unique 'State' values
unique_state = pd.Series(state.unique())

# Function to clean extra spaces
def clean_extra_spaces(state):
    state_series_cleaned = state.str.strip().str.replace(r'\s+', ' ', regex=True)
    return state_series_cleaned

# Define the regex pattern for valid state names
pattern = r'^[A-Za-z ]+$'

# Validate 'State' using the regex pattern
def state_validation(state):
    # Convert the array to a pandas Series (to use .str methods)
    state_names = clean_extra_spaces(state)
    
    # Create a boolean mask for invalid state names
    invalid_state_names = state_names[~state_names.str.match(pattern)]

    if not invalid_state_names.empty:
        print("Invalid State Names:")
        print(invalid_state_names)
    else:
        print("Valid State Names: YES")

# Method to check missing names
def check_missing_state_names(state):
    missing_state_names = state.isnull().sum()
    print(f"\nMissing State Names: {missing_state_names}")

# Define the regex pattern for extra spaces
pattern_extra_spaces_state = r'(?:^\s+|\s{2,}|\s+$)'

# Method to check for extra spaces
def check_extra_spaces(state):
    state_extra_spaces = pd.Series(state)

    # Create a boolean mask for city names with extra spaces
    state_with_extra_spaces = state_extra_spaces[state_extra_spaces.str.contains(pattern_extra_spaces_state, regex=True)]
    
    if not state_with_extra_spaces.empty:
        print("\nState Names with Extra Spaces")
        print(state_with_extra_spaces)
    else:
        print("\nNo Extra Spaces Detected")

# Apply the validation to unique customer names
state_validation(unique_state)

# Apply the method to check missing customer names
check_missing_state_names(state)

# Check for extra spaces
check_extra_spaces(state)

# Extract the 'Postal Code' column
postal_code = data['Postal Code']

# Extract the unique 'Postal Code' values and convert to strings
unique_postal_code = pd.Series(postal_code.unique()).astype(str)

# Use regex to remove '.0' from numbers
def remove_decimals(postal_code):
    return postal_code.str.replace(r'^(\d+)\.0$', r'\1', regex=True)

# Function to clean extra spaces
def clean_extra_spaces(postal_code):
    # Convert to strings and clean extra spaces
    postalcode_series_cleaned = postal_code.astype(str).str.strip().str.replace(r'\s+', ' ', regex=True)
    return remove_decimals(postalcode_series_cleaned)

# Define the regex pattern for 'Postal Code'
pattern = r'^\d{5}$'

# Validate 'Postal Code' using the regex pattern
def postal_code_validation(postal_code):
    print("\nInitial Assessment\n")
    # Convert the cleaned postal code to a pandas Series
    postal_code_series = pd.Series(clean_extra_spaces(postal_code))
    
    # Create a boolean mask for invalid postal codes
    invalid_postal_code = postal_code_series[~postal_code_series.str.match(pattern)]

    if not invalid_postal_code.empty:
        print("Standard Postal Codes: NO")
        print(invalid_postal_code)
    else:
        print("Standard Postal Codes: YES")

# Define the regex pattern for extra spaces
pattern_extra_spaces_postalcode = r'(?:^\s+|\s{2,}|\s+$)'

# Method to check for extra spaces
def check_extra_spaces(postal_code):
    postalcode_extra_spaces = pd.Series(postal_code.astype(str))

    # Create a boolean mask for extra spaces
    postalcode_with_extra_spaces = postalcode_extra_spaces[postalcode_extra_spaces.str.contains(pattern_extra_spaces_postalcode, regex=True)]
    
    if not postalcode_with_extra_spaces.empty:
        print("\nPostal Codes with Extra Spaces")
        print(postalcode_with_extra_spaces)
    else:
        print("\nNo Extra Spaces Detected")

def format_postal_codes(postal_code):
    print("Final Result")
    # Convert all postal codes to strings
    postal_code_str = postal_code.astype(str)

    # Use a lambda function to apply the logic
    formatted_postal_codes = postal_code_str.apply(lambda x: x.zfill(5) if len(x) == 4 else x)
    return formatted_postal_codes

# Apply the function to format postal codes
formatted_postal_codes = format_postal_codes(postal_code)

# Check if the formatted postal codes are empty
if formatted_postal_codes.empty:
    print("\nNo Postal Codes to Format")
else:
    print("\nFormatted Postal Codes")
    print(formatted_postal_codes)


# Method to check missing postal codes
def check_missing_postal_code(postal_code):
    missing_postal_code = postal_code.isnull().sum()
    print(f"\nMissing Postal Codes: {missing_postal_code}")

# Apply the validation to unique postal codes
postal_code_validation(unique_postal_code)

# Apply the method to check missing postal codes
check_missing_postal_code(postal_code)

# Apply the function to format postal codes
format_postal_codes(postal_code)

# Check for extra spaces
check_extra_spaces(postal_code)

# Extract the 'Region' column
region = data['Region']

# Extract the unique 'Region' values
unique_region = pd.Series(region.unique())

# Function to clean extra spaces
def clean_extra_spaces(region):
    region_series_cleaned = region.str.strip().str.replace(r'\s+', ' ', regex=True)
    return region_series_cleaned

# Define the regex pattern for valid region names
pattern = r'^[A-Za-z]+$'

# Validate 'Region' using the regex pattern
def region_validation(region):
    # Convert the array to a pandas Series (to use .str methods)
    region_names = clean_extra_spaces(region)
    
    # Create a boolean mask for invalid region names
    invalid_region_names = region_names[~region_names.str.match(pattern)]

    if not invalid_region_names.empty:
        print("Invalid Region Names:")
        print(invalid_region_names)
    else:
        print("Valid Region Names: YES")

# Define the regex pattern for extra spaces
pattern_extra_spaces_region = r'(?:^\s+|\s{2,}|\s+$)'

# Method to check missing names
def check_missing_region_names(region):
    missing_region_names = region.isnull().sum()
    print(f"\nMissing Region Names: {missing_region_names}")

# Method to check for extra spaces
def check_extra_spaces(region):
    region_extra_spaces = pd.Series(region)

    # Create a boolean mask for region names with extra spaces
    region_with_extra_spaces = region_extra_spaces[region_extra_spaces.str.contains(pattern_extra_spaces_region, regex=True)]
    
    if not region_with_extra_spaces.empty:
        print("\nRegion Names with Extra Spaces")
        print(region_with_extra_spaces)
    else:
        print("\nNo Extra Spaces Detected")

# Apply the validation to unique region names
region_validation(unique_region)

# Apply the method to check missing region names
check_missing_region_names(region)

# Check for extra spaces
check_extra_spaces(region)

# Extract the 'Product ID' column
product_id = data['Product ID']

# Extract the unique 'Product ID' values
unique_product_id = pd.Series(product_id.unique())

# Function to clean extra spaces
def clean_extra_spaces(product_id):
    productid_series_cleaned = product_id.str.strip().str.replace(r'\s+', ' ', regex=True)
    return productid_series_cleaned

# Define the regex pattern for 'Product ID'
product_id_pattern = r'^[A-Z]{3}-[A-Z]{2}-\d{8}$'

# Validate 'Product ID' using the regex pattern
def product_id_validation(product_id):
    # Convert the array to a pandas Series (to use .str methods)
    product_id_series = pd.Series(product_id)
    
    # Create a boolean mask for invalid product IDs
    invalid_product_id = product_id_series[~product_id_series.str.match(product_id_pattern)]

    if not invalid_product_id.empty:
        print("Standard Customer IDs: NO")
        print(invalid_product_id)
    else:
        print("Standard Customer IDs: YES")

# Define the regex pattern for extra spaces
pattern_extra_spaces_productid = r'(?:^\s+|\s{2,}|\s+$)'

# Method to check for extra spaces
def check_extra_spaces(product_id):
    productid_extra_spaces = pd.Series(product_id)

    # Create a boolean mask for extra spaces
    productid_with_extra_spaces = productid_extra_spaces[productid_extra_spaces.str.contains(pattern_extra_spaces_productid, regex=True)]
    
    if not productid_with_extra_spaces.empty:
        print("\nCustomer IDs with Extra Spaces")
        print(productid_with_extra_spaces)
    else:
        print("\nNo Extra Spaces Detected")

# Method to check missing values
def check_missing_product_id(product_id):
        missing_product_id = product_id.isnull().sum()
        print(f"\nMissing Customer IDs: {missing_product_id}")

# Apply the validation to unique product IDs
product_id_validation(unique_product_id)

# Apply the method to check missing product id's
check_missing_product_id(product_id)

# Check for extra spaces
check_extra_spaces(product_id)

# Extract the 'Category' column
category = data['Category']

# Extract the unique 'Category' values
unique_category = pd.Series(category.unique())

# Function to clean extra spaces
def clean_extra_spaces(category):
    category_series_cleaned = category.str.strip().str.replace(r'\s+', ' ', regex=True)
    return category_series_cleaned

# Define the regex pattern for valid category names
pattern = r'^[A-Za-z]+(?: [A-Za-z]+)?$'

# Validate 'Category' using the regex pattern
def category_validation(category):
    # Convert the array to a pandas Series (to use .str methods)
    category_names = clean_extra_spaces(category)
    
    # Create a boolean mask for invalid category names
    invalid_category_names = category_names[~category_names.str.match(pattern)]

    if not invalid_category_names.empty:
        print("Invalid Category Names:")
        print(invalid_category_names)
    else:
        print("Valid Region Names: YES")

# Define the regex pattern for extra spaces
pattern_extra_spaces_category = r'(?:^\s+|\s{2,}|\s+$)'

# Method to check missing names
def check_missing_category_names(category):
    missing_category_names = region.isnull().sum()
    print(f"\nMissing Category Names: {missing_category_names}")

# Method to check for extra spaces
def check_extra_spaces(category):
    category_extra_spaces = pd.Series(category)

    # Create a boolean mask for region names with extra spaces
    category_with_extra_spaces = category_extra_spaces[category_extra_spaces.str.contains(pattern_extra_spaces_category, regex=True)]
    
    if not category_with_extra_spaces.empty:
        print("\nCategory Names with Extra Spaces:")
        print(category_with_extra_spaces)
    else:
        print("\nNo Extra Spaces Detected")

# Apply the validation to unique region names
category_validation(unique_category)

# Apply the method to check missing region names
check_missing_category_names(category)

# Check for extra spaces
check_extra_spaces(category)

# Extract the 'Sub-Category' column
sub_category = data['Sub-Category']

# Extract the unique 'Sub-Category' values
unique_sub_category = pd.Series(sub_category.unique())

# Function to clean extra spaces
def clean_extra_spaces(sub_category):
    sub_category_series_cleaned = sub_category.str.strip().str.replace(r'\s+', ' ', regex=True)
    return sub_category_series_cleaned

# Define the regex pattern for valid sub_category names
pattern = r'^[A-Za-z]+$'

# Validate 'Sub-Category' using the regex pattern
def sub_category_validation(sub_category):
    # Convert the array to a pandas Series (to use .str methods)
    sub_category_names = clean_extra_spaces(sub_category)
    
    # Create a boolean mask for invalid sub_category names
    invalid_sub_category = sub_category_names[~sub_category_names.str.match(pattern)]

    if not invalid_sub_category.empty:
        print("Invalid Sub-Category Names:")
        print(invalid_sub_category)
    else:
        print("Valid Sub-Category Names: YES")

# Define the regex pattern for extra spaces
pattern_extra_spaces_sub_category = r'(?:^\s+|\s{2,}|\s+$)'

# Method to check missing names
def check_missing_sub_category(sub_category):
    missing_sub_category = sub_category.isnull().sum()
    print(f"\nMissing Sub-Category Names: {missing_sub_category}")

# Method to check for extra spaces  
def check_extra_spaces(sub_category):
    sub_category_extra_spaces = pd.Series(sub_category)

    # Create a boolean mask for region names with extra spaces
    sub_category_with_extra_spaces = sub_category_extra_spaces[sub_category_extra_spaces.str.contains(pattern_extra_spaces_sub_category, regex=True)]
    
    if not sub_category_with_extra_spaces.empty:
        print("\nSub-Category with Extra Spaces")
        print(sub_category_with_extra_spaces)
    else:
        print("\nNo Extra Spaces Detected")

# Apply the validation to unique region names
sub_category_validation(unique_sub_category)

# Apply the method to check missing region names
check_missing_sub_category(sub_category)

# Check for extra spaces
check_extra_spaces(sub_category)

# Extract the 'Product Name' column
product_name = data['Product Name']

# Extract the unique product names
unique_product_names = pd.Series(product_name.unique())

def validate_product_name(input_product):
    if input_product in unique_product_names.values:
        print("\nNo Invalid Products")
    else:
        print(f"{input_product} Inavlid Product Names")

# Example of validating a product name
validate_product_name(unique_product_names)  # Change the input as needed

# Extract the 'Sales' column as a Series
sales = pd.Series(['Sales'])

# Define a regex pattern to detect non-numeric characters
non_numeric_pattern = r'[^0-9.]'

# Function to validate the 'Sales' Series for non-numeric characters
def validate_numeric_pattern(sales):
    sales_str = sales.astype(str)
    invalid_format = sales_str[sales_str.str.contains(non_numeric_pattern, regex=True)]

    if not invalid_format.empty:
        print("\nInvalid Format Found:")
        print(invalid_format)
    else:
        print("\nValues follow numeric pattern")

# Function to convert all values to numeric
def format_sales(sales):
    numeric_sales_format = pd.to_numeric(sales, errors='coerce')
    return numeric_sales_format

# Function to check if all values are numeric and identify any non-numeric entries
def check_value_type(sales):
    sales_converted = format_sales(sales)
    non_numeric_values = sales_converted[sales_converted.isna()]

    if not non_numeric_values.empty:
        print("\nNon-numeric values found:")
        print(non_numeric_values)
    else:
        print("\nAll values are numeric")

# Execute validation and conversion
validate_numeric_pattern(sales)
check_value_type(sales)


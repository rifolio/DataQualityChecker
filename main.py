import pandas as pd
from geotext import GeoText
import re

class DataTypeIdentifier:
    def __init__(self, data):
        self.data = data
        self.column_data_types = {}
        self.data_type_counts = {'Date': 0, 'Price': 0, 'Telephone Number': 0, 'Email Address': 0,
                                 'Link (URL)': 0, 'Country': 0, 'City': 0, 'Name or Text': 0}
        self.missing_value_counts = {}
        self.missing_columns_flag = False

    def identify_data_types(self):
        column_names = self.data.columns
        for col in column_names:
            missing_values = self.data[col].isnull().sum()
            if missing_values > 0:
                self.missing_value_counts[col] = missing_values
                self.missing_columns_flag = True

            if self.check_date(col):
                self.column_data_types[col] = 'Date'
                self.data_type_counts['Date'] += 1
            elif self.check_price(col):
                self.column_data_types[col] = 'Price'
                self.data_type_counts['Price'] += 1
            elif self.check_telephone_number(col):
                self.column_data_types[col] = 'Telephone Number'
                self.data_type_counts['Telephone Number'] += 1
            elif self.check_email_address(col):
                self.column_data_types[col] = 'Email Address'
                self.data_type_counts['Email Address'] += 1
            elif self.check_url(col):
                self.column_data_types[col] = 'Link (URL)'
                self.data_type_counts['Link (URL)'] += 1
            elif self.check_country(col):
                self.column_data_types[col] = 'Country'
                self.data_type_counts['Country'] += 1
            elif self.check_city(col):
                self.column_data_types[col] = 'City'
                self.data_type_counts['City'] += 1
            else:
                self.column_data_types[col] = 'Name or Text'
                self.data_type_counts['Name or Text'] += 1

    def check_date(self, col):
        return self.data[col].apply(lambda x: isinstance(x, str) and pd.notna(pd.to_datetime(x, errors='coerce'))).any()

    def check_telephone_number(self, col):
        return self.data[col].astype(str).str.match(r'^(\+?[0-9() -]{7,15})$').any()

    def check_email_address(self, col):
        return self.data[col].astype(str).str.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$').any()

    def check_url(self, col):
        return self.data[col].astype(str).str.match(
            r'^(https?://)?(www\.)?[\w\-]+(\.[\w\-]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?$').any()

    def check_price(self, col):
        return self.data[col].astype(str).str.match(r'^[$€]?\d+(\.\d{1,3})?[$€]?$').any()

    def check_country(self, col):
        return (self.data[col].astype(str).str.strip().apply(lambda x: x.title() in GeoText(x).countries)).any()

    def check_city(self, col):
        return (self.data[col].astype(str).str.strip().apply(lambda x: x.title() in GeoText(x).cities)).any()

    def print_results(self):
        for col, data_type in self.column_data_types.items():
            print(f"{col}: {data_type}")

        print("\nData Type Counts:")
        for data_type, count in self.data_type_counts.items():
            print(f"{data_type}: {count}")

        if self.missing_columns_flag:
            print("\nMissing Value Counts:")
            for col, missing_count in self.missing_value_counts.items():
                print(f"Columns name is {col}, and it has {missing_count} missing values")
        else:
            print("\nNo missing values found in any column.")

    def check_type(self):
        email_count = self.data_type_counts['Email Address']
        phone_count = self.data_type_counts['Telephone Number']
        
        if email_count > 4:
            print("There are 4 or more email addresses.")
        if email_count > 0 and phone_count > 0:
            print('More than 0 emails and phone numbers')

def main():
    df = pd.read_csv('data1.csv')
    data_identifier = DataTypeIdentifier(df)
    data_identifier.identify_data_types()
    data_identifier.print_results()
    data_identifier.check_type()

if __name__ == "__main__":
    main()
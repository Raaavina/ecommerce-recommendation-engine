#Feature Store script
# src/data_processing.py
import pandas as pd
import numpy as np
import os

# src/data_processing.py
class DataPipeline:
    def __init__(self, data_dir="data"): # Change "../data" to "data"
        self.data_dir = data_dir

    def load_clean_data(self):
        """Loads and prepares basic transaction matrix assets"""
        sales_path = os.path.join(self.data_dir, "sales_history.csv")
        if not os.path.exists(sales_path):
            raise FileNotFoundError("Clean sales assets missing! Run notebooks first.")
            
        df_sales = pd.read_csv(sales_path)
        return df_sales

    def build_user_item_matrix(self, df_sales):
        """Generates high-performance interaction matrix arrays"""
        active_customers = df_sales['CustomerID'].value_counts()[df_sales['CustomerID'].value_counts() > 5].index
        df_filtered = df_sales[df_sales['CustomerID'].isin(active_customers)]
        
        matrix = df_filtered.pivot_table(
            index='CustomerID', 
            columns='StockCode', 
            values='Quantity', 
            aggfunc='sum'
        ).fillna(0)
        return matrix
# Import Required Libraries
import pandas as pd
from pathlib import Path 

# Simple function to scrape particular wikipedia html table using pandas.read_html()
def wiki_scraper(url,  table_order):
    dataframe = pd.read_html(url)[table_order-1]
    return dataframe

wiki_url = "http://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue"
table_order = 2 # Select the 2nd table in the wiki page 
companies = wiki_scraper(wiki_url, table_order)

# Remove columns we don't need
companies = companies[['Name', 'Revenue (USD millions)']]

# Take only the top 40 companies 
companies = companies.head(41)

# Re-Format and rename revenue column
companies['Revenue (USD millions)'] = companies['Revenue (USD millions)']*1000000
companies = companies.rename(columns={'Revenue (USD millions)':'revenueUSD'})

# Create probabilities column to dictate the probability that a support tickets is from that company
# Probability is based on the revenue of the company - larger revenue means a company is more likely to send a support ticket
companies['probability'] = companies['revenueUSD']/companies['revenueUSD'].sum()

# Save down scraped data to csv
data_path = Path('Data/')
companies.to_csv(data_path / '01_raw.csv', index = False)

import yfinance as yf
import pandas as pd
import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import warnings

# Ignore FutureWarning messages
warnings.filterwarnings('ignore', category=FutureWarning)


def make_graph(stock_data, revenue_data, stock_name):
    """Create graph for data visualization."""

    # Filter stock price data up to June 14, 2021
    specific_stock_data = stock_data[stock_data.Date <= '2021-06-14']

    # Filter revenue data up to April 30, 2021
    specific_revenue_data = revenue_data[revenue_data.Date <= '2021-04-30']

    # Create two vertically stacked plots that share the same x-axis
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    # Stock price graph
    # Convert dates to datetime and closing prices to float
    axes[0].plot(
        pd.to_datetime(specific_stock_data.Date),
        specific_stock_data.Close.astype('float'),
        label='Share Price',
        color='blue'
    )

    # Add the y-axis label and chart title
    axes[0].set_ylabel('Price ($US)')
    axes[0].set_title(f"{stock_name} - Historical Share Price")

    # Revenue graph
    # Convert dates to datetime and revenue values to float
    axes[1].plot(
        pd.to_datetime(specific_revenue_data.Date),
        specific_revenue_data.Revenue.astype('float'),
        label='Share Price',
        color='blue'
    )

    # Add the y-axis label and chart title
    axes[1].set_ylabel('Revenue ($US Millions)')
    axes[1].set_title(f"{stock_name} - Historical Revenue")

    # Adjust spacing to prevent chart elements from overlapping
    plt.tight_layout()

    # Display both graphs
    plt.show()


# -------------------- TESLA STOCK DATA --------------------

# Create a Ticker object for Tesla using its stock symbol
tesla = yf.Ticker('TSLA')

# Retrieve Tesla's maximum available historical stock data
tesla_data = tesla.history(period='max')

# Convert the Date index into a regular column
tesla_data.reset_index(inplace=True)

# Display the first five rows to inspect the retrieved data
print(tesla_data.head())


# -------------------- TESLA REVENUE DATA --------------------

# URL containing Tesla's historical revenue table
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"

# Send an HTTP GET request to retrieve the webpage
response = requests.get(url, timeout=30)

# Raise an exception if the HTTP response indicates an error
response.raise_for_status()

# Extract the HTML source code from the response
html_data = response.text

# Parse the HTML so its elements can be searched
soup = BeautifulSoup(html_data, 'html.parser')

# Create an empty DataFrame to store Tesla's revenue data
tesla_revenue = pd.DataFrame(columns=['Date', 'Revenue'])

# Find the second table body and iterate through its rows
for row in soup.find_all('tbody')[1].find_all('tr'):

    # Extract all table cells from the current row
    col = row.find_all('td')

    # Extract the date from the first cell
    date = col[0].text

    # Extract the revenue value from the second cell
    revenue = col[1].text

    # Add the extracted date and revenue to the DataFrame
    tesla_revenue = pd.concat(
        [tesla_revenue, pd.DataFrame({'Date': [date], 'Revenue': [revenue]})],
        ignore_index=True
    )


# Remove commas and dollar signs from revenue values
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(
    r',|\$', "", regex=True
)

# Remove rows containing missing values
tesla_revenue.dropna(inplace=True)

# Remove rows where the revenue value is an empty string
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

# Print the last five rows to inspect the revenue data
print(tesla_revenue.tail()) 

# Generate Tesla's stock price and revenue graphs
make_graph(tesla_data, tesla_revenue, tesla.info.get('displayName'))


# -------------------- GAMESTOP STOCK DATA --------------------

# Create a Ticker object for GameStop using its stock symbol
gamestop = yf.Ticker('GME')

# Retrieve GameStop's maximum available historical stock data
gme_data = gamestop.history(period='max')

# Convert the Date index into a regular column
gme_data.reset_index(inplace=True)

# Print the GameStop stock data for inspection
print(gme_data)


# -------------------- GAMESTOP REVENUE DATA --------------------

# URL containing GameStop's historical revenue table
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"

# Send an HTTP GET request to retrieve the webpage
response2 = requests.get(url, timeout=30)

# Raise an exception if the HTTP response indicates an error
response2.raise_for_status()

# Extract the HTML source code from the response
html_data2 = response2.text

# Parse the HTML source code using BeautifulSoup
soup2 = BeautifulSoup(html_data2, 'html.parser')

# Create an empty DataFrame to store GameStop's revenue data
gme_revenue = pd.DataFrame(columns=['Date', 'Revenue'])

# Find the second table body and iterate through its rows
for row in soup2.find_all('tbody')[1].find_all('tr'):

    # Extract all table cells from the current row
    col = row.find_all('td')

    # Extract the date from the first cell
    date = col[0].text

    # Extract the revenue value from the second cell
    revenue = col[1].text

    # Add the extracted date and revenue to the DataFrame
    gme_revenue = pd.concat(
        [gme_revenue, pd.DataFrame({'Date': [date], 'Revenue': [revenue]})],
        ignore_index=True
    )


# Remove commas and dollar signs from revenue values
gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(
    r',|\$', "", regex=True
)

# Remove rows containing missing values
gme_revenue.dropna(inplace=True)

# Remove rows where the revenue value is an empty string
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]

# Print GameStop's revenue data for inspection
print(gme_revenue) 

# Generate GameStop's stock price and revenue graphs
make_graph(gme_data, gme_revenue, gamestop.info.get('displayName'))
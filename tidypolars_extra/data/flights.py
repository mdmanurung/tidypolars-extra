from pathlib import Path
from ..io import read_data
from ..tibble_df import tibble

DATA_DIR = Path(__file__).parent

def __load_flights__():
    flights = read_data(fn=DATA_DIR / "flights.csv", sep=',', silently=True)
    flights.__doc__ = """
    Monthly Airline Passenger Numbers 1949-1960

    ## Description

    The classic Box & Jenkins airline data. Monthly totals of
    international airline passengers, 1949 to 1960.

    ## Format

    A data frame with 144 observations on 3 variables.

    |------------|--------------------------------------|
    | Column     | Description                          |
    |============|======================================|
    | year       | Year of observation (1949–1960)      |
    | month      | Month of observation (Jan–Dec)       |
    | passengers | Number of passengers (in thousands)  |
    |------------|--------------------------------------|

    ## Source

    Box, G. E. P., Jenkins, G. M. and Reinsel, G. C. (1976)
    *Time Series Analysis, Forecasting and Control*. Third Edition.
    Holden-Day. Series G.
    """
    return tibble(flights)

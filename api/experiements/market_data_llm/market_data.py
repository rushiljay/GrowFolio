import yfinance as yf
from langchain_core.tools import tool

@tool()
def get_industry_sector_description(ticker: str) -> dict:
    """
    Get the sector, industry, and long description of a company from its ticker
    """
    stock = yf.Ticker(ticker)

    about_company = {
        'sector': stock.info['sector'],
        'industry': stock.info['industry'],
        'longBusinessSummary': stock.info['longBusinessSummary']
    }
    return about_company


if __name__ == '__main__':
    print(get_industry_sector_description('AAPL'))
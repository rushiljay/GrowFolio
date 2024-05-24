import yfinance as yf
from langchain_core.tools import tool

# TODO: add more detialed descriptions to the functions

def get_stock(ticker: str):
    try:
        return yf.Ticker(ticker)
    except Exception:
        return {
            'Error': f"This {ticker} does not exist"
        }

@tool
def get_industry_sector_description(ticker: str) -> dict:
    """
    Get the sector, industry, and long description of a company from its ticker
    """
    stock = get_stock(ticker)
    about_company = {
        'sector': stock.info['sector'],
        'industry': stock.info['industry'],
        'longBusinessSummary': stock.info['longBusinessSummary']
    }
    return about_company

@tool
def get_company_risk(ticker: str) -> dict:
    """
    Get the risk assessment of a company from its ticker
    """
    stock = get_stock(ticker)
    
    risk_assessment = {
        'auditRisk': stock.info['auditRisk'],
        'boardRisk': stock.info['boardRisk'],
        'compensationRisk': stock.info['compensationRisk'],
        'shareHolderRightsRisk': stock.info['shareHolderRightsRisk'],
        'overallRisk': stock.info['overallRisk']
    }
    return risk_assessment


@tool
def get_price_info(ticker: str) -> dict:
    """
    Get detailed price information of a company from its ticker
    """
    stock = get_stock(ticker)
    
    price_info = {
        'priceHint': stock.info['priceHint'],
        'previousClose': stock.info['previousClose'],
        'open': stock.info['open'],
        'dayLow': stock.info['dayLow'],
        'dayHigh': stock.info['dayHigh'],
        'regularMarketPreviousClose': stock.info['regularMarketPreviousClose'],
        'regularMarketOpen': stock.info['regularMarketOpen'],
        'regularMarketDayLow': stock.info['regularMarketDayLow'],
        'regularMarketDayHigh': stock.info['regularMarketDayHigh']
    }
    return price_info

@tool
def get_financial_data(ticker: str) -> dict:
    """
    Get financial data of a company from its ticker
    """
    stock = get_stock(ticker)
    
    financial_data = {
        'dividendRate': stock.info['dividendRate'],
        'dividendYield': stock.info['dividendYield'],
        'exDividendDate': stock.info['exDividendDate'],
        'payoutRatio': stock.info['payoutRatio'],
        'fiveYearAvgDividendYield': stock.info['fiveYearAvgDividendYield'],
        'beta': stock.info['beta'],
        'trailingPE': stock.info['trailingPE'],
        'forwardPE': stock.info['forwardPE'],
        'volume': stock.info['volume'],
        'regularMarketVolume': stock.info['regularMarketVolume'],
        'averageVolume': stock.info['averageVolume'],
        'averageVolume10days': stock.info['averageVolume10days'],
        'averageDailyVolume10Day': stock.info['averageDailyVolume10Day'],
        'marketCap': stock.info['marketCap'],
        'fiftyTwoWeekLow': stock.info['fiftyTwoWeekLow'],
        'fiftyTwoWeekHigh': stock.info['fiftyTwoWeekHigh'],
        'priceToSalesTrailing12Months': stock.info['priceToSalesTrailing12Months'],
        'fiftyDayAverage': stock.info['fiftyDayAverage'],
        'twoHundredDayAverage': stock.info['twoHundredDayAverage'],
        'trailingAnnualDividendRate': stock.info['trailingAnnualDividendRate'],
        'trailingAnnualDividendYield': stock.info['trailingAnnualDividendYield'],
        'currency': stock.info['currency'],
        'enterpriseValue': stock.info['enterpriseValue'],
        'profitMargins': stock.info['profitMargins'],
        'floatShares': stock.info['floatShares'],
        'sharesOutstanding': stock.info['sharesOutstanding'],
        'sharesShort': stock.info['sharesShort'],
        'sharesShortPriorMonth': stock.info['sharesShortPriorMonth'],
        'sharesShortPreviousMonthDate': stock.info['sharesShortPreviousMonthDate'],
        'dateShortInterest': stock.info['dateShortInterest'],
        'sharesPercentSharesOut': stock.info['sharesPercentSharesOut'],
        'heldPercentInsiders': stock.info['heldPercentInsiders'],
        'heldPercentInstitutions': stock.info['heldPercentInstitutions'],
        'shortRatio': stock.info['shortRatio'],
        'shortPercentOfFloat': stock.info['shortPercentOfFloat'],
        'impliedSharesOutstanding': stock.info['impliedSharesOutstanding'],
        'bookValue': stock.info['bookValue'],
        'priceToBook': stock.info['priceToBook'],
        'lastFiscalYearEnd': stock.info['lastFiscalYearEnd'],
        'nextFiscalYearEnd': stock.info['nextFiscalYearEnd'],
        'mostRecentQuarter': stock.info['mostRecentQuarter'],
        'earningsQuarterlyGrowth': stock.info['earningsQuarterlyGrowth'],
        'netIncomeToCommon': stock.info['netIncomeToCommon'],
        'trailingEps': stock.info['trailingEps'],
        'forwardEps': stock.info['forwardEps'],
        'pegRatio': stock.info['pegRatio'],
        'lastSplitFactor': stock.info['lastSplitFactor'],
        'lastSplitDate': stock.info['lastSplitDate'],
        'enterpriseToRevenue': stock.info['enterpriseToRevenue'],
        'enterpriseToEbitda': stock.info['enterpriseToEbitda'],
        '52WeekChange': stock.info['52WeekChange'],
        'SandP52WeekChange': stock.info['SandP52WeekChange'],
        'lastDividendValue': stock.info['lastDividendValue'],
        'lastDividendDate': stock.info['lastDividendDate'],
        'gmtOffSetMilliseconds': stock.info['gmtOffSetMilliseconds'],
        'totalCash': stock.info['totalCash'],
        'totalCashPerShare': stock.info['totalCashPerShare'],
        'ebitda': stock.info['ebitda'],
        'totalDebt': stock.info['totalDebt'],
        'quickRatio': stock.info['quickRatio'],
        'currentRatio': stock.info['currentRatio'],
        'totalRevenue': stock.info['totalRevenue'],
        'debtToEquity': stock.info['debtToEquity'],
        'revenuePerShare': stock.info['revenuePerShare'],
        'returnOnAssets': stock.info['returnOnAssets'],
        'returnOnEquity': stock.info['returnOnEquity'],
        'freeCashflow': stock.info['freeCashflow'],
        'operatingCashflow': stock.info['operatingCashflow'],
        'earningsGrowth': stock.info['earningsGrowth'],
        'revenueGrowth': stock.info['revenueGrowth'],
        'grossMargins': stock.info['grossMargins'],
        'ebitdaMargins': stock.info['ebitdaMargins'],
        'operatingMargins': stock.info['operatingMargins'],
        'trailingPegRatio': stock.info['trailingPegRatio']
    }
    return financial_data

#TODO: make this return DIRECT OUTPUT

@tool
def get_current_price(ticker: str) -> float:
    """
    Get the current price of a stock from its ticker
    """
    stock = get_stock(ticker)
    current_price = stock.info['currentPrice']
    return current_price

@tool
def get_analyst_recommendations(ticker: str) -> dict:
    """
    Get analyst recommendation for a stock from its ticker
    """
    stock = get_stock(ticker)
    
    analyst_recommendations = {
        'targetHighPrice': stock.info['targetHighPrice'],
        'targetLowPrice': stock.info['targetLowPrice'],
        'targetMeanPrice': stock.info['targetMeanPrice'],
        'targetMedianPrice': stock.info['targetMedianPrice'],
        'recommendationMean': stock.info['recommendationMean'],
        'recommendationKey': stock.info['recommendationKey'],
        'numberOfAnalystOpinions': stock.info['numberOfAnalystOpinions']
    }
    return analyst_recommendations

# if __name__ == '__main__':
#     print(get_industry_sector_description('AAPL'))
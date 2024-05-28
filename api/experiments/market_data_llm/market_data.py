from sys import exception
import langchain
import langchain.globals
import yfinance as yf
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
# from langchain.agents import initialize_agent, Tool
# from pandas import describe_option
from dotenv import load_dotenv, find_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain.agents import create_json_agent
# from langchain_community.agent_toolkits import JsonToolkit
# from langchain_community.tools.json.tool import JsonSpec
# from pydantic import BaseModel, Field
# from typing import Optional, Dict, Any
import time
import os
import streamlit as st
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
import logging



@tool
#TODO: if the ticker is a real ticker already, just return it
def get_ticker (company_name: str) -> str:
    """Gets the ticker of a company name from Yahoo Finance"""
    #print(company_name)
    time.sleep(0.1)
    try:
        url = "https://query2.finance.yahoo.com/v1/finance/search"
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        params = {"q": company_name, "quotes_count": 1, "country": "United States"}
        res = requests.get(url=url, params=params, headers={'User-Agent': user_agent})
        data = res.json()
        return data['quotes'][0]['symbol']
    except:
        try:
            stock = yf.Ticker(company_name)
            return company_name
        except:
            return company_name+" not found, try guessing the name or the ticker symbol of the company, and try with other function."

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

    company_risk = {}

    keys = ['auditRisk', 'boardRisk', 'compensationRisk', 'shareHolderRightsRisk', 'overallRisk']

    for key in keys:
        try:
            company_risk[key] = stock.info[key]
        except KeyError:
            company_risk[key] = 'N/A'

    return company_risk

@tool
def get_price_info(ticker: str) -> dict:
    """
    Get detailed price information of a company from its ticker
    """
    stock = get_stock(ticker)

    price_info = {}

    keys = ['priceHint','previousClose','open','dayLow','dayHigh','regularMarketPreviousClose','regularMarketOpen','regularMarketDayLow','regularMarketDayHigh']
    
    for key in keys:
        try:
            price_info[key] = stock.info[key]
        except KeyError:
            price_info[key] = 'N/A'
    
    return price_info

@tool
def get_financial_data(ticker: str) -> dict:
    """
    Get financial data of a company from its ticker
    
    Args:
        ticker (str): The ticker symbol of the company
    
    Returns:
        dict: A dictionary containing the financial data of the company, including various metrics such as dividend rate, dividend yield, market cap, etc.
    """
    stock = get_stock(ticker)
    
    financial_data = {}
    keys = [
        'dividendRate', 'dividendYield', 'exDividendDate', 'payoutRatio', 'fiveYearAvgDividendYield',
        'beta', 'trailingPE', 'forwardPE', 'volume', 'regularMarketVolume', 'averageVolume',
        'averageVolume10days', 'averageDailyVolume10Day', 'marketCap', 'fiftyTwoWeekLow', 'fiftyTwoWeekHigh',
        'priceToSalesTrailing12Months', 'fiftyDayAverage', 'twoHundredDayAverage', 'trailingAnnualDividendRate',
        'trailingAnnualDividendYield', 'currency', 'enterpriseValue', 'profitMargins', 'floatShares',
        'sharesOutstanding', 'sharesShort', 'sharesShortPriorMonth', 'sharesShortPreviousMonthDate',
        'dateShortInterest', 'sharesPercentSharesOut', 'heldPercentInsiders', 'heldPercentInstitutions',
        'shortRatio', 'shortPercentOfFloat', 'impliedSharesOutstanding', 'bookValue', 'priceToBook',
        'lastFiscalYearEnd', 'nextFiscalYearEnd', 'mostRecentQuarter', 'earningsQuarterlyGrowth',
        'netIncomeToCommon', 'trailingEps', 'forwardEps', 'pegRatio', 'lastSplitFactor', 'lastSplitDate',
        'enterpriseToRevenue', 'enterpriseToEbitda', '52WeekChange', 'SandP52WeekChange', 'lastDividendValue',
        'lastDividendDate', 'gmtOffSetMilliseconds', 'totalCash', 'totalCashPerShare', 'ebitda', 'totalDebt',
        'quickRatio', 'currentRatio', 'totalRevenue', 'debtToEquity', 'revenuePerShare', 'returnOnAssets',
        'returnOnEquity', 'freeCashflow', 'operatingCashflow', 'earningsGrowth', 'revenueGrowth',
        'grossMargins', 'ebitdaMargins', 'operatingMargins', 'trailingPegRatio'
    ]

    for key in keys:
        try:
            financial_data[key] = stock.info[key]
        except KeyError:
            financial_data[key] = 'N/A'
    return financial_data

#TODO: make this return DIRECT OUTPUT

@tool#(return_direct=True)
def get_current_price(ticker: str) -> float:
    """
    Get the current price of a stock from its ticker
    """
    stock = get_stock(ticker)
    current_price = stock.info['currentPrice']
    return current_price

@tool
def get_analyst_recommendations_summary(ticker: str) -> dict:
    """
    Get analyst recommendation for a stock from its ticker
    """
    stock = get_stock(ticker)

    keys = ['targetHighPrice', 'targetLowPrice', 'targetMeanPrice', 'targetMedianPrice', 'recommendationMean', 'recommendationKey', 'numberOfAnalystOpinions']
    
    analyst_recommendations = {}

    for key in keys:
        try:
            analyst_recommendations[key] = stock.info[key]
        except KeyError:
            analyst_recommendations[key] = 'N/A'

    return analyst_recommendations

# This can directly be fed into the charting tool
@tool#(return_direct=True)
def get_history(ticker: str, time_period="3mo", time_interval="1d") -> dict:
    """
    Get the history of a stock from its ticker
    period: data period to download (either use period parameter or use start and end) Valid periods are:
“1d”, “5d”, “1mo”, “3mo”, “6mo”, “1y”, “2y”, “5y”, “10y”, “ytd”, “max”
interval: data interval (1m data is only for available for last 7 days, and data interval <1d for the last 60 days) Valid intervals are:
“1m”, “2m”, “5m”, “15m”, “30m”, “60m”, “90m”, “1h”, “1d”, “5d”, “1wk”, “1mo”, “3mo”

Period must be greater than interval
    """
    stock = get_stock(ticker)

    history = stock.history(period=time_period, inteval=time_interval)

    return history.to_dict()

@tool#(return_direct=True)
def get_actions(ticker: str) -> dict:
    """
    Get the actions of a stock from its ticker
    """
    stock = get_stock(ticker)

    actions = stock.actions

    return actions.to_dict()

@tool#(return_direct=True)
def get_income_stmt(ticker: str) -> dict:
    """
    Get the income statement of a stock from its ticker
    """
    stock = get_stock(ticker)

    income_stmt = stock.income_stmt

    return income_stmt.to_dict()

@tool#(return_direct=True)
def get_quarterly_income_stmt(ticker: str) -> dict:
    """
    Get the quarterly income statement of a stock from its ticker
    """
    stock = get_stock(ticker)
    quarterly_income_stmt = stock.quarterly_income_stmt
    
    return quarterly_income_stmt.to_dict()

@tool#(return_direct=True)
def get_balance_sheet(ticker: str) -> dict:
    """
    Get the balance sheet of a stock from its ticker
    """
    stock = get_stock(ticker)
    balance_sheet = stock.balance_sheet
    
    return balance_sheet.to_dict()

@tool#(return_direct=True)
def get_quarterly_balance_sheet(ticker: str) -> dict:
    """
    Get the quarterly balance sheet of a stock from its ticker
    """
    stock = get_stock(ticker)
    quarterly_balance_sheet = stock.quarterly_balance_sheet
    
    return quarterly_balance_sheet.to_dict()

@tool#(return_direct=True)  
def get_cashflow(ticker: str) -> dict:
    """
    Get the cashflow of a stock from its ticker
    """
    stock = get_stock(ticker)
    cashflow = stock.cashflow
    
    return cashflow.to_dict()

@tool#(return_direct=True)
def get_quarterly_cashflow(ticker: str) -> dict:
    """
    Get the quarterly cashflow of a stock from its ticker
    """
    stock = get_stock(ticker)
    quarterly_cashflow = stock.quarterly_cashflow
    
    return quarterly_cashflow.to_dict()

@tool#(return_direct=True)
def get_earnings_dates(ticker: str) -> dict:
    """
    Get the earnings of a stock from its ticker
    """
    stock = get_stock(ticker)
    earnings = stock.earnings_dates
    
    return earnings.to_dict()

@tool#(return_direct=True)
def get_recommendations(ticker: str) -> dict:
    """
    Get the recommendations of a stock from its ticker
    """
    stock = get_stock(ticker)
    recommendations = stock.recommendations
    
    return recommendations.to_dict()

@tool#(return_direct=True)
def get_news(ticker: str) -> dict:
    """
    Get the news of a stock from its ticker
    """
    stock = get_stock(ticker)
    news = stock.news
    
    return news

# TODO: need to implement holders and options

if __name__ == '__main__':

    logger = logging.getLogger('yfinance')
    logger.disabled = True
    logger.propagate = False
    # load_dotenv(find_dotenv())
    # llm = ChatGroq(temperature=1, model_name="llama3-70b-8192")

    # api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
    # wikitool = WikipediaQueryRun(api_wrapper=api_wrapper)

    # tools = [get_ticker,
    #         get_industry_sector_description,
    #         get_company_risk,
    #         get_price_info,
    #         get_financial_data,
    #         get_current_price,
    #         get_analyst_recommendations_summary,
    #         get_history,
    #         get_actions,
    #         get_income_stmt,
    #         get_quarterly_income_stmt,
    #         get_balance_sheet,
    #         get_quarterly_balance_sheet,
    #         get_cashflow,
    #         get_quarterly_cashflow,
    #         get_earnings_dates,
    #         get_recommendations,
    #         get_news, 
    #         wikitool]
    
    # # print(os.getcwd())

    # with open('system.txt', 'r') as file:
    #     system_message = file.read()
    
    # prompt = ChatPromptTemplate.from_messages(
    #     [
    #         ("system", system_message),
    #         ("placeholder", "{chat_history}"),
    #         ("human", "{input}"),
    #         ("placeholder", "{agent_scratchpad}"),
    #     ]
    # )    
    # agent = create_tool_calling_agent(llm, tools, prompt)
    # agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # chain = agent_executor

    # ###

    with st.sidebar:
        groq_api_key = st.text_input("Groq API Key", key="groq_api_key", type="password")

    # Streamlit page setup
    st.title('GrowFolio Chatbot')
    st.write("Ask any finance related questions!")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "Hi, I'm a chatbot who can give you stock market data and perform research. How can I help you?"}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    IN_PROGRESS = False

    if prompt := st.chat_input(placeholder="What is the stock price of Apple?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        if IN_PROGRESS:
            st.info("Please wait for the current request to finish.")
            st.stop()
        else:
            IN_PROGRESS = True
            st.chat_message("user").write(prompt)

        print(IN_PROGRESS)

        if not groq_api_key:
            st.info("Please add your Groq API key to continue.")
            st.stop()

        llm = ChatGroq(temperature=0.5, model_name="llama3-70b-8192", groq_api_key=groq_api_key) # plz dont change

        api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
        wikitool = WikipediaQueryRun(api_wrapper=api_wrapper)

        tools = [get_ticker,
                get_industry_sector_description,
                get_company_risk,
                get_price_info,
                get_financial_data,
                get_current_price,
                get_analyst_recommendations_summary,
                get_history,
                get_actions,
                get_income_stmt,
                get_quarterly_income_stmt,
                get_balance_sheet,
                get_quarterly_balance_sheet,
                get_cashflow,
                get_quarterly_cashflow,
                get_earnings_dates,
                get_recommendations,
                get_news, 
                wikitool]
        
        # print(os.getcwd())

        with open('system.txt', 'r') as file:
            system_message = file.read()
        
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_message),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}"),
            ]
        )    
        agent = create_tool_calling_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        chain = agent_executor
        with st.chat_message("assistant"):
            #print(st.session_state.messages[-1])
            response = ''
            i = 0
            REATTEMPT_LIMIT = 3
            query = st.session_state.messages[-1]['content']
            while i < REATTEMPT_LIMIT:
                print(query, i)
                try:
                    if (IN_PROGRESS):
                        tempQuery = query
                        if (i == 0):
                            tempQuery += " (Use get_news or wikipedia for more nuanced questions, use tools in formulating a cohesive response with latest data)"
                        response = chain.invoke({"input": tempQuery})['output']
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        response = response.replace("$","\$")


                        # for word in response.split(" "):
                        #     time.sleep(0.01)
                        #     st.write_stream(word + " ")

                        def stream_data():
                            for word in response.split(" "):
                                    yield word + " "
                                    time.sleep(0.02)
                        
                        st.write_stream(stream_data)
                        #st.write(response)
                        IN_PROGRESS = False
                        i = 0
                    break
                except Exception as e:
                    query = "USE LESS TOOLS!!! Don't use \"get_news\"!!! " + query
                    #tools = tools[1:-1]
                    print(e)
                    response = e
                    i += 1

    # ###

    # while True:
    #     query = input("Human: ")
    #     # print("Human: " + query)
    #     try:
    #         print("Chatbot: " + chain.invoke({"input": query + " (Use tools as necessary in formulating a cohesive response)"})['output'])
    #     except Exception as e:
    #         print(e)
    #         print("There was an error with your query")

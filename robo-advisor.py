from zipline.api import *
from configparser import ConfigParser
import datetime
import ast

def initialize(context):
    print ("Starting the robo advisor")
    set_benchmark(symbol("AAPL"))
    core_series = symbols('VTI', 'VXUS', 'BND', 'BNDX')


    '''
    core_series_weights = {0: (0,0,0.686,0.294),
                           1: (0.059,0.039,0.617,0.265),
                           2: (0.118,0.078,0.549,0.235),
                           3: (0.176,0.118,0.480,0.206),
                           4: (0.235,0.157,0.412,0.176),
                           5: (0.294,0.196,0.343,0.147),
                           6: (0.353,0.235,0.274,0.118),
                           7: (0.412,0.274,0.206,0.088),
                           8: (0.470,0.314,0.137,0.059),
                           9: (0.529,0.353,0.069,0.029),
                           10: (0.588,0.392,0,0)}
    '''

    context.stocks = core_series
    #risk_based_allocation = core_series_weights
    risk_based_allocation = section_to_dict('CORE_SERIES')
    risk_level = 5

    context.target_allocation = dict(zip(context.stocks, risk_based_allocation[risk_level]))
    context.bought = False

    schedule_function(
    func=before_trading_starts,
    date_rule=date_rules.every_day(),
    time_rule=time_rules.market_open(hours=1),
    )


def handle_data(context, data):
    if (context.bought == False):
        print("Buying for the first time!")
        for stock in context.stocks:
            if (context.target_allocation[stock] == 0):
                continue
            amount = (context.target_allocation[stock] * context.portfolio.cash) / data.current(stock, 'price')
            order(stock, int(amount))
            print("Buying " + str(int(amount)) + " shares of " + str(stock))
        context.bought = True


def before_trading_starts(context, data):
    #total value of portfolio
    value = context.portfolio.portfolio_value
    #calculating current weights for each position
    for stock in context.stocks:
        if (context.target_allocation[stock] == 0):
            continue
        current_holdings = data.current(stock,'close') * context.portfolio.positions[stock].amount
        weight = current_holdings/value
        growth = float(weight) / float(context.target_allocation[stock])
        #if weights of any position exceed threshold, trigger rebalance
        if (growth >= 1.05 or growth <= 0.95):
            rebalance(context, data)
            break
    print("No need to rebalance!")

def rebalance(context, data):
    for stock in context.stocks:
        current_weight = (data.current(stock, 'close') * context.portfolio.positions[stock].amount) / context.portfolio.portfolio_value
        target_weight = context.target_allocation[stock]
        distance = current_weight - target_weight
        if (distance > 0):
            amount = -1 * (distance * context.portfolio.portfolio_value) / data.current(stock,'close')
            if (int(amount) == 0):
                continue
            print("Selling " + str(int(amount)) + " shares of " + str(stock))
            order(stock, int(amount))
    for stock in context.stocks:
        current_weight = (data.current(stock, 'close') * context.portfolio.positions[stock].amount) / context.portfolio.portfolio_value
        target_weight = context.target_allocation[stock]
        distance = current_weight - target_weight
        if (distance < 0):
            amount = -1 * (distance * context.portfolio.portfolio_value) / data.current(stock,'close')
            if (int(amount) == 0):
                continue
            print("Buying " + str(int(amount)) + " shares of " + str(stock))
            order(stock, int(amount))

def section_to_dict(section):
    config = ConfigParser()
    config.read('universe-config.ini')
    out_dict = {}
    for key in config[section]:
        out_dict[int(key)] = ast.literal_eval(config['CORE_SERIES'][key])
	return(out_dict)

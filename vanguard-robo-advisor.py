# Put any initialization logic here.  The context object will be passed to
# the other methods in your algorithm.
import datetime
import pytz
import numpy as np



def initialize(context):
    # Initialize algorithm parameters
    # setting symbol lists
    core_series = symbols('VTI', 'VXUS', 'BND', 'BNDX')
    crsp_series = symbols('VUG', 'VTV', 'VB', 'VEA', 'VWO', 'BSV', 'BIV', 'BLV', 'VMBS', 'BNDX')
    #universe risk based allocation
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

    crsp_series_weights = {0: (0,0,0,0,0,0.273,0.14,0.123,0.15,0.294),
                           1: (0.024,0.027,0.008,0.03,0.009,0.245,0.126,0.111,0.135,0.265),
                           2: (0.048,0.054,0.016,0.061,0.017,0.218,0.112,0.099,0.12,0.235),
                           3: (0.072,0.082,0.022,0.091,0.027,0.191,0.098,0.086,0.105,0.206),
                           4: (0.096,0.109,0.03,0.122,0.035,0.164,0.084,0.074,0.09,0.176),
                           5: (0.120,0.136,0.038,0.152,0.044,0.126,0.07,0.062,0.075,0.147),
                           6: (0.143,0.163,0.047,0.182,0.053,0.109,0.056,0.049,0.06,0.118),
                           7: (0.167,0.190,0.055,0.213,0.061,0.082,0.042,0.037,0.045,0.088),
                           8: (0.191,0.217,0.062,0.243,0.071,0.055,0.028,0.024,0.030,0.059),
                           9: (0.215,0.245,0.069,0.274,0.079,0.027,0.014,0.013,0.015,0.029),
                           10: (0.239,0.272,0.077,0.304,0.088,0,0,0,0,0)}

    #set universe and risk level
    context.stocks = crsp_series
    risk_based_allocation = crsp_series_weights
    risk_level = 1
    #Saves the weights to easily access during rebalance
    context.target_allocation = dict(zip(context.stocks, risk_based_allocation[risk_level]))
    #To make initial purchase
    context.bought = False
    #Calculates the distance vector every day before trading starts
    schedule_function(
    func=before_trading_starts,
    date_rule=date_rules.every_day(),
    time_rule=time_rules.market_open(hours=1))


def before_trading_starts(context, data):
    #total value of portfolio
    value = context.portfolio.portfolio_value + context.portfolio.cash
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


def rebalance(context, data):
    for stock in context.stocks:
        current_weight = (data.current(stock, 'close') * context.portfolio.positions[stock].amount) / context.portfolio.portfolio_value
        target_weight = context.target_allocation[stock]
        distance = current_weight - target_weight
        if (distance > 0):
            amount = -1 * (distance * context.portfolio.portfolio_value) / data.current(stock,'close')
            if (int(amount) == 0):
                continue
            log.info("Selling " + str(int(amount)) + " shares of " + str(stock))
            order(stock, int(amount))
    for stock in context.stocks:
        current_weight = (data.current(stock, 'close') * context.portfolio.positions[stock].amount) / context.portfolio.portfolio_value
        target_weight = context.target_allocation[stock]
        distance = current_weight - target_weight
        if (distance < 0):
            amount = -1 * (distance * context.portfolio.portfolio_value) / data.current(stock,'close')
            if (int(amount) == 0):
                continue
            log.info("Buying " + str(int(amount)) + " shares of " + str(stock))
            order(stock, int(amount))


def handle_data(context, data):
    #initial purchase of portfolio
    if not context.bought:
        for stock in context.stocks:
            #Allocate cash based on weight, and then divide by price to buy shares
            amount = (context.target_allocation[stock] * context.portfolio.cash) / data.current(stock,'price')
            #only buy if cash is allocated
            if (amount != 0):
                order(stock, int(amount))
                #log purchase
            log.info("buying " + str(int(amount)) + " shares of " + str(stock))
        #now won't purchase again and again
        context.bought = True

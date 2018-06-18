from zipline.api import *
from configparser import ConfigParser
import datetime
import ast

def initialize(context):
    print ("Starting the robo advisor")

    core_series = symbols('VTI', 'VXUS', 'BND', 'BNDX')
    crsp_series = symbols('VUG', 'VTV', 'VB', 'VEA', 'VWO', 'BSV', 'BIV', 'BLV', 'VMBS', 'BNDX')
    s&p_series = symbols('VOO', 'VXF', 'VEA', 'VWO', 'BSV', 'BIV', 'BLV', 'VMBS', 'BNDX')
    russell_series = symbols('VONG', 'VONV', 'VTWO', 'VEA', 'VTWO', 'VEA', 'VWO', 'BSV', 'BIV', 'BLV', 'VMBS', 'BNDX')
    income_series = symbols('VTI', 'VYM', 'VXUS', 'VYMI', 'BND', 'VTC', 'BNDX')
    tax_series = symbols('VUG', 'VTV', 'VB', 'VEA', 'VWO', 'VTEB')

    context.stocks = crsp_series
    #risk_based_allocation = core_series_weights
    risk_based_allocation = section_to_dict('CRSP_SERIES')
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
        out_dict[int(key)] = ast.literal_eval(config[section][key])
    return(out_dict)

from zipline.api import *
import datetime

def initialize(context):
    context.stocks = symbols('VTI', 'VXUS', 'BND', 'BNDX')
    context.bought = False

    risk_level = 5
    risk_based_allocation = {0: (0,0,0.686,0.294),
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
    #Saves the weights to easily access during rebalance
    context.target_allocation = dict(zip(context.stocks, risk_based_allocation[risk_level]))


def handle_data(context, data):
    if not context.bought:
        for stock in context.stocks:
            if (context.target_allocation[stock] == 0):
                continue
            amount = (context.portfolio.cash * context.target_allocation[stock]) / data.current(stock, 'price')
            order(stock, int(amount))
            print("Ordered " + str(int(amount)) + " shares of " + str(stock))
        context.bought = True

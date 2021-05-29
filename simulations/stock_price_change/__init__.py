import random
import statistics

NO_OF_TRADING_DAY_YR = 252
NO_OF_TRADING_DAY_MN = 21

class Stocks:
    def __init__(self, start_price, annual_volatility):
        self.start_price = start_price
        self.daily_volatility = self.__getDailyVolatility(annual_volatility)

    def __getDailyVolatility(self, annual_volatility):
        return annual_volatility/(NO_OF_TRADING_DAY_YR**(1/2))

    def trade(self, days):
        instant_price = self.start_price
        for i in range(days):
            volatility = instant_price*(self.daily_volatility/100)
            instant_price += random.uniform(-volatility, volatility)
        return instant_price



def run(iterations):
    stocks = Stocks(620, 30)
    monthly_trades = []
    for i in range(iterations):
        monthly_trades.append(stocks.trade(NO_OF_TRADING_DAY_MN))
    print('Mean: ', round(statistics.mean(monthly_trades),2))
    print('Std Deviation: ', round(statistics.pstdev(monthly_trades),2))
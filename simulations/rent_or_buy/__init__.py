import yaml
import matplotlib.pyplot as plt
import random
import statistics

class Rent:
    def __init__(self):
        with open("globals/rent_or_buy_config.yaml", "r") as yamlfile:
            self.config = yaml.load(yamlfile, Loader=yaml.FullLoader)
        self.initial_rent = self.config['initial_rent']
        self.down_payment = self.config['down_payment']
        self.annual_appreciation = self.config['annual_appreciation']
        self.market_returns = self.config['market_returns']
        self.period = self.config['period']


    def __get_monthly_appreciation(self):
        monthly_appr_min = self.annual_appreciation[0]/12
        monthly_appr_max = self.annual_appreciation[1]/12
        value = random.uniform( monthly_appr_min, monthly_appr_max)
        return value


    def __get_monthly_market_returns(self):
        monthly_market_returns_min = self.market_returns[0]/12
        monthly_market_returns_max = self.market_returns[1]/12
        value = random.uniform(monthly_market_returns_min, monthly_market_returns_max)
        return value


    def monthly_wealth(self, emi):
        predicted_monthly_wealth = []
        wallet = self.down_payment

        # Month 1
        rent = self.initial_rent
        monthly_saving = emi-rent
        wallet += (wallet * self.__get_monthly_market_returns()) + monthly_saving
        predicted_monthly_wealth.append(wallet)

        # Month 2-N
        for i in range(1,self.period*12):
            rent = rent * (1 + self.__get_monthly_appreciation())
            monthly_saving = emi - rent
            wallet += (wallet * self.__get_monthly_market_returns()) + monthly_saving
            predicted_monthly_wealth.append(wallet)

        return predicted_monthly_wealth


class Buy:
    def __init__(self):
        with open("globals/rent_or_buy_config.yaml", "r") as yamlfile:
            self.config = yaml.load(yamlfile, Loader=yaml.FullLoader)
        self.house_price = self.config['house_price']
        self.down_payment = self.config['down_payment']
        self.interest_rate = self.config['interest_rate']
        self.annual_appreciation = self.config['annual_appreciation']
        self.annual_costs = self.config['annual_costs']
        self.period = self.config['period']


    def EMI(self):
        loan_amount = self.house_price - self.down_payment
        monthly_interest_rate = self.interest_rate/12
        r = monthly_interest_rate
        n = self.period * 12

        emi = loan_amount * r * ((1+r)**n)/(((1+r)**n) - 1)
        return emi


    def __get_monthly_appreciation(self):
        monthly_appr_min = self.annual_appreciation[0]/12
        monthly_appr_max = self.annual_appreciation[1]/12
        value = random.uniform( monthly_appr_min, monthly_appr_max)
        return value


    def monthly_wealth(self):
        predicted_monthly_wealth = []
        ownership = self.down_payment/self.house_price
        monthly_ownership_gain = (1-ownership)/(self.period*12)
        # Month 1
        property_value = self.house_price
        predicted_monthly_wealth.append(self.down_payment)

        # Month 2-N
        for i in range(1,self.period*12):
            property_value += property_value * self.__get_monthly_appreciation()
            ownership += monthly_ownership_gain
            wealth = property_value * ownership
            predicted_monthly_wealth.append(wealth)

        return predicted_monthly_wealth


class Graph:
    def __init__(self):
        pass

    def plot(self, x1, y1, x2, y2, x3, y3, x4, y4):
        # # Colors
        # Blue:   light: #ADD8E6
        #         dark : #7BC8F6
        # Red :   light: #FF6347
        #         dark : #EF4026
        plt.plot(x1, y1, color='#7BC8F6', label='buyer wealth max')
        plt.plot(x2, y2, color='#ADD8E6', label='buyer wealth min')
        plt.plot(x3, y3, color='#EF4026', label='renter wealth max')
        plt.plot(x4, y4, color='#FF6347', label='renter wealth min')
        plt.xlabel('year')
        plt.ylabel('total wealth')
        plt.title('Rent')
        plt.legend()
        plt.show()



def run(iterations):
    rent = Rent()
    buy = Buy()
    graph = Graph()

    emi = buy.EMI()
    period = 30

    buyer_predictions  = [[] for x in range(0, period)]
    renter_predictions = [[] for x in range(0, period)]

    for _ in range(iterations):
        buyer_monthly_wealth = buy.monthly_wealth()
        renter_monthly_wealth = rent.monthly_wealth(emi)

        buyer_yearly_wealth = [buyer_monthly_wealth[x] for x in range(0,period*12,12)]
        renter_yearly_wealth = [renter_monthly_wealth[x] for x in range(0,period*12,12)]

        for year in range(period):
            buyer_predictions[year].append(buyer_yearly_wealth[year])
            renter_predictions[year].append(renter_yearly_wealth[year])

    buyer_mean = [statistics.mean(x) for x in buyer_predictions]
    renter_mean = [statistics.mean(x) for x in renter_predictions]

    buyer_std = [statistics.pstdev(x) for x in buyer_predictions]
    renter_std = [statistics.pstdev(x) for x in renter_predictions]

    y1 = [buyer_mean[x]+buyer_std[x] for x in range(period)]
    y2 = [buyer_mean[x]-buyer_std[x] for x in range(period)]
    y3 = [renter_mean[x]+renter_std[x] for x in range(period)]
    y4 = [renter_mean[x]-renter_std[x] for x in range(period)]

    x = [x for x in range(2020,2050)]

    graph.plot(x, y1, x, y2, x, y3, x, y4)

    # print("Buyer: ", buyer_std)
    # print("Renter: ", renter_std)


from requests import Session
from signalr import Connection

"""
This module holds the code which defines a market scraper bot.
The bot can open a websocket connection with the bittrex server
and receives data packets that first tell it what the order book
of the particular market is, then receives updates to that order
book. It maintains an internal state of a portion of the market
order book and writes that to disk to keep a timeline.
"""


class ScraperBot:


    def __init__(self, market_str):

        self.market = market_str


    def scrape(self):

        with Session() as session:
            connection = Connection("http://www.bittrex.com/signalr/", session)
            corehub = connection.register_hub('coreHub')
            connection.start()

            connection.received += self.handle_received
            connection.error += self.print_error

            corehub.server.invoke('SubscribeToExchangeDeltas', self.market)
            corehub.server.invoke('QueryOrderState', self.market)
            corehub.server.invoke('QueryExchangeState', self.market)

            while True:
                connection.wait(1)


    def handle_received(self, **kwargs):

        if "R" in kwargs.keys():
            pass

        if kwargs["M"]:

    #     if 'M' in kwargs.keys() and kwargs['M']:
    #         print("Nounce = ",
    #               kwargs['M'][0]['A'][0]['Nounce'])
    #
    #         if kwargs['M'][0]['M'] != 'updateSummaryState':
    #             print('received: ', kwargs)
    #     else:
    #         print("empty")


    def print_error(self, error):
        print('error: ', error)


import threading
import random
import time

class OrderBook:
    def __init__(self):
        self.orders = []
        self.lock = threading.Lock()

    def addOrder(self, order_type, ticker, quantity, price):
        order = (order_type, ticker, quantity, price)
        with self.lock:
            ticker_found = False
            for item in self.orders:
                if item[0] == ticker:
                    ticker_found = True
                    item[1][order_type].append(order)
                    break
            if not ticker_found:
                self.orders.append([ticker, {'buy': [], 'sell': [order]} if order_type == 'sell' else {'buy': [order], 'sell': []}])

    def matchOrder(self):
        """Match buy and sell orders based on the conditions."""
        with self.lock:
            matched_orders = []
            for ticker_entry in self.orders:
                ticker = ticker_entry[0]
                orders = ticker_entry[1]

                buy_orders = sorted(orders['buy'], key=lambda x: x[3], reverse=True)
                sell_orders = sorted(orders['sell'], key=lambda x: x[3])

                i, j = 0, 0
                while i < len(buy_orders) and j < len(sell_orders):
                    buy_order = buy_orders[i]
                    sell_order = sell_orders[j]

                    if buy_order[3] >= sell_order[3]:
                        matched_orders.append((buy_order, sell_order))
                        i += 1
                        j += 1
                    else:
                        break 

                ticker_entry[1]['buy'] = buy_orders[i:]
                ticker_entry[1]['sell'] = sell_orders[j:]

            for buy, sell in matched_orders:
                print(f'Matched Buy Order: {buy}, Sell Order: {sell}')

def simulate_order(book):
    order_type = random.choice(['buy', 'sell'])
    ticker = random.choice(['AAPL', 'GOOG', 'AMZN', 'TSLA', 'MSFT'])
    quantity = random.randint(1, 100)
    price = random.randint(100, 1500)
    book.addOrder(order_type, ticker, quantity, price)
    time.sleep(random.random()) 


if __name__ == "__main__":
    book = OrderBook()

    threads = []
    for _ in range(100): 
        t = threading.Thread(target=simulate_order, args=(book,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    book.matchOrder()
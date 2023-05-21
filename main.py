class Order:
    def __init__(self, i, t, d, w):
        self.i = i
        self.t = t
        self.d = d
        self.w = w
        self.T = t

    def print_order(self):
        print(f"The {self.i} order : t = {self.t} days, d = {self.d} days, w = {self.w} UAH. T[{self.i}] = {self.T}")


class Car:
    def __init__(self, i):
        self.i = i
        self.S = []  #розклад замовлень
        self.busyness = 0
        self.reward = 0
        self.is_delay = False

    def update_reward(self):
        reward = 0
        for order in self.S:
            if order.T <= order.d:
                reward += order.w
        self.reward = reward

    def print_s(self):
        print(f"Car {self.i} has busyness {self.busyness}, has reward: {self.reward}, UAH and such schedule:")
        for order in self.S:
            order.print_order()

def sort_orders(orders):
    """Sorts orders due to w/d value. Starts with the order with the biggest value."""
    sorted_list = sorted(orders, key=lambda x: x.w/x.d, reverse=True)
    return sorted_list


def create_schedule(orders, cars):  # orders are sorted
    """Creates schedule for cars. Computes a busyness for every car and add next order to the car
    with the smallest busyness"""
    order_i = 0
    # for every car add first order
    for car in cars:
        car.S.append(orders[order_i])
        car.busyness += orders[order_i].t
        orders[order_i].T = car.busyness
        if car.busyness > orders[order_i].d:
            car.is_delay = True
        car.busyness += orders[order_i].t  # back to post station
        order_i += 1
    # find the car with the smallest busyness, and it's index
    min_busyness = min(cars, key=lambda x: x.busyness, default=None)
    min_index = cars.index(min_busyness)
    # to sort orders between cars (add an order to a car with the smallest busyness)
    for i in range(len(cars), len(orders)):
        cars[min_index].S.append(orders[i])
        cars[min_index].busyness += orders[i].t
        orders[i].T = cars[min_index].busyness
        if cars[min_index].busyness > orders[i].d:
            cars[min_index].is_delay = True
        cars[min_index].busyness += orders[i].t
        min_busyness = min(cars, key=lambda x: x.busyness, default=None)
        min_index = cars.index(min_busyness)
    for car in cars:
        car.update_reward()


def create_data():
    orders = []
    # create orders
    orders.extend([
        Order(1, 12, 22, 300),
        Order(2, 24, 85, 550),
        Order(3, 36, 159, 350),
        Order(4, 42, 228, 625),
        Order(5, 30, 119, 400),
        Order(6, 24, 252, 525),
        Order(7, 30, 202, 650),
        Order(8, 48, 310, 700),
        Order(9, 10, 350, 800)
    ])
    orders = sort_orders(orders)
    # create cars
    cars = []
    cars.extend([
        Car(1),
        Car(2)
    ])
    return orders, cars


if __name__ == '__main__':
    # create schedule for every car
    orders, cars = create_data()
    create_schedule(orders, cars)
    # results
    for car in cars:
        if not car.is_delay:
            car.print_s()
        else:
            # car.optimization()
            car.print_s()




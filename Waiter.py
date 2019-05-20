import queue

import MoveScript
import constants


class Waiter:
    def __init__(self, x, y, w, map):
        self.x = x
        self.y = y
        self.w = w
        self.image = constants.S_WAITER
        self.drawable = True
        self.ordersqueue = queue.Queue(0)
        self.map=map

    def __str__(self):
        return "Waiter x: " + str(self.x) + " y: " + str(self.y) + " w: " + str(self.w)

    def addorder(self, order):
        self.ordersqueue.put(order)

    def do(self):
        if not self.ordersqueue.empty():
            print(self)
            getattr(self, self.ordersqueue.get())()

    def forward(self):
        print("forward")
        if self.w == 0:
            self.y = self.y - 1
        if self.w == 1:
            self.x = self.x + 1
        if self.w == 2:
            self.y = self.y + 1
        if self.w == 3:
            self.x = self.x - 1

    def left(self):
        print("left")
        if self.w > 0:
            self.w = self.w - 1
        else:
            self.w = 3

    def right(self):
        print("right")
        if self.w < 3:
            self.w = self.w + 1
        else:
            self.w = 0

    def go_to(self, x, y, w):
        self.ordersqueue.queue.clear()
        orderlist = MoveScript.go_to_pos(self.x, self.y, self.w, x, y, w,self.map)
        if not orderlist is None:
            for order in orderlist:
                self.addorder(order)

# isinstance(x, X) czy obiekt x jest klasy X
# pass koniec definicji

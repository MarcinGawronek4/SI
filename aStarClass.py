from anytree import Node, RenderTree
import PriorityQueue
import constants


def astar(istate, fstate):
    fringe = PriorityQueue.PriorityQueue()
    explored = []
    fringe.insert(Node(istate))
    while True:
        if fringe.isEmpty():
            return None
        elem = fringe.delete()
        if elem.name == fstate:
            print("done?")
            return elem
        explored.append(elem)
        for stan in elem.name.succ():
            stan.priority = stan.cost + stan.f(fstate)
            x = Node(stan, elem)
            infringe = any(st.name == x.name for st in fringe.queue)
            inexplored = any(st.name == x.name for st in explored)
            if not infringe and not inexplored:
                fringe.insert(x)
            else:
                if infringe:
                    i = next(fringe.queue.index(z) for z in fringe.queue if z.name == x.name)
                    if x.name.priority < fringe.queue[i].name.priority:
                        fringe.queue[i] = x


class State:
    action = ""
    cost = 0
    priority = 0

    def succ(self):
        return []

    def f(self, other):
        return 0

    def __eq__(self, other):
        return None

    def __str__(self):
        return self.action

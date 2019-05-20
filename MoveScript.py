import constants
import main
from aStarClass import astar, State


def get_elements(x, y):
    return [objects for objects in objectlist if objects.x == x and objects.y == y]


def forward(istate):
    state = istate.copy()
    way = state.w
    if way == 0:
        state.y = state.y - 1
    if way == 1:
        state.x = state.x + 1
    if way == 2:
        state.y = state.y + 1
    if way == 3:
        state.x = state.x - 1
    state.action = constants.O_MOVE_FORWARD
    objectlist = get_elements(state.x, state.y)
    if (constants.MAP_WIDTH > state.y >= 0 and constants.MAP_HEIGHT > state.x >= 0 and
            not any(getattr(objects, "walkcost", 0) == -1 for objects in objectlist)):
        movecost = 0
        for obj in objectlist:
            mcmeth = getattr(obj, "walkcost", 0)
            movecost = movecost + getattr(obj, "walkcost", 0)
        state.cost = state.cost + movecost + 1
        return state
    else:
        return None


def left(istate):
    state = istate.copy()
    if state.w > 0:
        state.w = state.w - 1
    else:
        state.w = 3
    state.cost = state.cost + 0.5
    state.action = constants.O_TURN_LEFT
    return state


def right(istate):
    state = istate.copy()
    if state.w < 3:
        state.w = state.w + 1
    else:
        state.w = 0
    state.cost = state.cost + 0.5
    state.action = constants.O_TURN_RIGHT
    return state


def succ(self):
    table = []
    result = []
    table.append(forward(self))
    table.append(left(self))
    table.append(right(self))
    for st in table:
        if not (st is None):
            result.append(st)
    return result


def manh(istate, fstate):
    return abs(istate.x - fstate.x) + abs(istate.y - fstate.y)


def equali(sobj, oobj):
    if sobj.x != oobj.x:
        return False
    if sobj.y != oobj.y:
        return False
    if sobj.w != oobj.w:
        return False
    return True


class MoveState(State):
    x = 0
    y = 0
    w = 0

    def succ(self):
        table = []
        result = []
        table.append(forward(self))
        table.append(left(self))
        table.append(right(self))
        for st in table:
            if not (st is None):
                result.append(st)
        return result

    def f(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __eq__(self, other):
        if self.x != other.x:
            return False
        if self.y != other.y:
            return False
        if self.w != other.w:
            return False
        return True

    def copy(self):
        obj = MoveState()
        obj.x = self.x
        obj.y = self.y
        obj.w = self.w
        obj.action = self.action
        obj.cost = self.cost
        obj.priority = self.priority
        return obj

    def __str__(self):
        return self.action


def go_to_pos(x, y, w, tx, ty, tw, map):
    global objectlist
    objectlist = map
    istate = MoveState()
    istate.x = x
    istate.y = y
    istate.w = w
    fstate = MoveState()
    fstate.x = tx
    fstate.y = ty
    fstate.w = tw
    global finals
    finals = fstate
    aresult = astar(istate, fstate)
    if aresult is None:
        return None
    orderlist = []
    while True:
        orderlist = [aresult.name.action] + orderlist
        aresult = aresult.parent
        if aresult.parent is None:
            break
    return orderlist


from sortedcontainers import SortedDict
from ordered_dict import OrderedDictWithRemove, Priority
from utils import Vertex
import numpy as np


order = SortedDict()


order[5] = 1232
order[2] = 45
order[7] = 777

#print(order.peekitem(index=0)[1])
#print(order)
#print(order.peekitem())

#print(len(order))

item = order.popitem(index=0)
#print(item)

#item = order.pop()

v = Vertex((3, 7))
pr = Priority(4, 10)

d = OrderedDictWithRemove()

d.insert(pos=(1, 5), priority=pr)

d.insert(pos=(1, 5), priority=pr)
d.remove((1,5))



print(d)

#print((4, 10) < (4, 2))

eps = 1e-10
print(eps * 10 ** 12)

a = np.inf
b = np.inf

print(abs(a - b) < 3)
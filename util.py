import hashlib
import collections
from ecdsa import NIST256p
print(NIST256p)
block1 = {'a':10,'b':39}
block2 = {'b':39,'a':10}

def orderBlock(block):
    return collections.OrderedDict(sorted(block.items(),key=lambda x:x[0]))

orderDict = lambda x: collections.OrderedDict(sorted(x.items(),key=lambda x:x[0]))


block1 = orderBlock(block1)
block2 = orderBlock(block2)
block3 = orderDict(block1)
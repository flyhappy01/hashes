#coding=utf-8

# 使用虚拟节点来是每个rs分配更均匀，增加了rs查找时的时间，二分查找会多几次
from hashlib import md5
from struct import unpack_from
from bisect import bisect_left

ITEMS = 10000000
NODES = 100
# 每个rs对应了1000个虚拟节点
VNODES = 1000
node_stat = [0 for i in range(NODES)]


def _hash(value):
    k = md5(str(value)).digest()
    ha = unpack_from(">I", k)[0]
    return ha

# rs环
ring = []
# 统计hash对应的rs
hash2node = {}

for n in range(NODES):
    for v in range(VNODES):
        h = _hash(str(n) + str(v))
        ring.append(h)
        # 注意这里统计到了n上，不是nv值加起来
        # 这里用map表示计算得到的虚拟节点和n的对应关系，不是直接v值。
        hash2node[h] = n
ring.sort()

for item in range(ITEMS):
    h = _hash(str(item))
    n = bisect_left(ring, h) % (NODES*VNODES)
    node_stat[hash2node[ring[n]]] += 1

print sum(node_stat), node_stat

_ave = ITEMS / NODES
_max = max(node_stat)
_min = min(node_stat)

print("Ave: %d" % _ave)
print("Max: %d\t(%0.2f%%)" % (_max, (_max - _ave) * 100.0 / _ave))
print("Min: %d\t(%0.2f%%)" % (_min, (_ave - _min) * 100.0 / _ave))

#coding=utf-8
# 假设流是均匀的情况下，计算rs被分配到的几率，平均值是多少，最大最小和平均值的差值百分比
from hashlib import md5
from struct import unpack_from
from bisect import bisect_left

ITEMS = 10000000
NODES = 100
node_stat = [0 for i in range(NODES)]


def _hash(value):
    k = md5(str(value)).digest()
    ha = unpack_from(">I", k)[0]
    return ha

ring = []
hash2node = {}

for n in range(NODES):
    # 计算hash
    h = _hash(n)
    # rs添加到ring中
    ring.append(h)
    # rs排序
    ring.sort()
    # 用一个字典记录每个hash值对应的rs
    # 这个的作用是统计每个rs节点，有多少hash值对应上
    hash2node[h] = n

for item in range(ITEMS):
    h = _hash(item)
    # 算出hash后，找到在ring中合适的位置，这个位置其实不用取模，bisect_right才需要
    n = bisect_left(ring, h) % NODES
    node_stat[hash2node[ring[n]]] += 1

_ave = ITEMS / NODES
_max = max(node_stat)
_min = min(node_stat)

print("Ave: %d" % _ave)
print("Max: %d\t(%0.2f%%)" % (_max, (_max - _ave) * 100.0 / _ave))
print("Min: %d\t(%0.2f%%)" % (_min, (_ave - _min) * 100.0 / _ave))

#coding=utf-8
# 包的md5值是均匀的，分给n个rs，机会平均就可以了
# 估计rs大概数量，然后将分区分配给rs
# 分区比rs多，一个rs有更多机会被选中
# 分区比rs少，有的rs没办法被选中吧
# 一致性hash无状态，如果修改权重，已有连接就会换rs了
from hashlib import md5
from struct import unpack_from
from bisect import bisect_left

ITEMS = 10000000
NODES = 100
LOG_NODE = 7
MAX_POWER = 32
PARTITION = MAX_POWER - LOG_NODE
node_stat = [0 for i in range(NODES)]


def _hash(value):
    k = md5(str(value)).digest()
    ha = unpack_from(">I", k)[0]
    return ha

ring = []
part2node = {}

# 分区数量是2^LOG_NODE,区加入到ring中，应该就是顺序的
for part in range(2 ** LOG_NODE):
    ring.append(part)
    part2node[part] = part % NODES

for item in range(ITEMS):
    # hash值，放到具体的分区里
    h = _hash(item) >> PARTITION
    part = bisect_left(ring, h)
    n = part % NODES
    node_stat[n] += 1

_ave = ITEMS / NODES
_max = max(node_stat)
_min = min(node_stat)

print("Ave: %d" % _ave)
print("Max: %d\t(%0.2f%%)" % (_max, (_max - _ave) * 100.0 / _ave))
print("Min: %d\t(%0.2f%%)" % (_min, (_ave - _min) * 100.0 / _ave))

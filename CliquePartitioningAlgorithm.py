# encoding: utf-8
import numpy as np
# 已经知道 矩阵为方阵即 n*n的矩阵
# 输入 数组的长度
n = input()
print ('the long of array n = ', n)
# Node 申请为一维数组 ，目前数组为空
Node = np.empty([n, 1], int)
for i in range(0, n):
    # Node 包含的数都为1（追加的）
    Node[i] = 1
for i in range(0, n):
    print ('Node [', i, '] =', Node[i])
# 构造二维数组的方法
# 前面的n为n行，后面的n为n列的意思，行不用体现
# 申请二维数组不用那么麻烦
# 可以这么做的原因是，该矩阵是方阵
NodeList = np.empty([n, n], int)  # 现在就可以认为 NodeList[n][n]
for i in range(0, n):
    for j in range(0, n):
        NodeList[i][j] = 2
for i in range(0, n):
    for i in range(0, n):
        print ('NodeList[',i, '][', j, '] = ', NodeList[i][j])
